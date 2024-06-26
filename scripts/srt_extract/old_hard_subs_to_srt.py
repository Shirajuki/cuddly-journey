from os import times
from PIL import Image
import pytesseract
import imagehash
import cv2
import numpy
import sys
import os
import pysrt
from imutils.video import FileVideoStream
from queue import Queue
from threading import Thread
import argparse

from lingua import Language, LanguageDetectorBuilder
from langdetect import detect
import pycld2 as cld2

sys.path.append('../ai_tools')
from edgegpt import edgegpt
sys.path.append('../srt_extract')

languages = [Language.VIETNAMESE, Language.ENGLISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

prompt = """
Here is a list of parsed vietnamese subtitle texts:
MESSAGE

Can you help me clean it up and from all the outputs guess what the correct message is? If you believe something is an abbrevation or doesn't fit in the message please do not include it. If you believe the parsed message came out bad and doesn't include anything meaninful, then write the answer as an empty space. Write your answer in the following format, take for example if the answer is "ANSWER":

START
ANSWER
END

OPTIONAL

Do not write your thoughts, only give the answer.
"""

a = [167,260,383,434,526,814,886,939,1044,1331,1376,1527,1957,1999,2048,2146,2663,2699,2730]
FIRST_FRAME = 0#a[10-2] #300 # Skip frames up to this point
FIRST_SUB_INDEX = 0#10-1
TEST = False
PREVIEW_MAX_SIZE = (1280, 720)

# The subtitles are within these bounds. The bounds are not super tight since
# Tesseract works better with some blank space around the text.
SUBTITLE_BOUNDS_LEFT = 0
SUBTITLE_BOUNDS_RIGHT = 1280
SUBTITLE_BOUNDS_TOP = 620-50
SUBTITLE_BOUNDS_BOTTOM = 720
# We force some space above and below the subtitles to be white before feeding
# the text images to Tesseract.
SUBTITLE_BLANK_SPACE_ABOVE = 20
SUBTITLE_BLANK_SPACE_BELOW = 20

# Hardcoded subtitles are not entirely white. To filter out subtitles we look
# for pixels that are as bright or brighter than this. Completely white is 255
SUBTITLES_MIN_VALUE = 200
# We add some blur to the subtitle images before feeding them to Tesseract since
# some pixels within the subtitles are not white enough. This also eliminates
# smaller groups of white pixels outside of the subtitles. A bigger value means
# more blur.
SUBTITLE_IMAGE_BLUR_SIZE = (11, 11)
# After blurring the image we make the image monochrome since that works better
# for Tesseract. This is the limit for what should be considered a (white)
# subtitle pixel after the blur.
SUBTITLES_MIN_VALUE_AFTER_BLUR = 55

# Only use Tesseract if the subtitle changes. This is for performance and also
# to avoid having single frames of Tesseract mistakes that get entered into the
# SRT file. To tell if two images are of the same subtitle we compare the image
# hashes of them. See https://pypi.org/project/ImageHash/ for more information.
IMAGE_HASH_SIZE = 32
MAX_HASH_DIFFERENCE_FOR_SAME_SUBTITLE = 20
NO_SUBTILE_FRAME_HASH = imagehash.hex_to_hash('0' * 256)

# Page segmentation mode (PSM) 13 means "Raw line. Treat the image as a single
# text line, bypassing hacks that are Tesseract-specific." See this link for
# other options:
# https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html#page-segmentation-method
TESSERACT_CONFIG = '--psm 13'
TESSERACT_CONFIG = ''

# Tesseract makes mistakes. Some are easy to fix. Keys in this dictionary will
# be replaced with their respective values.
COMMON_MISTAKES = {
    '-': '一',
    '+': '十',
    'F': '上',
    '，': '',
    '。': '',
    '”': '',
    "¬" : "",
    "一": "",
    "#": "",
    "°": "",
    "®": "",
    "%": "",
    "ø": "",
    ".": "",
    "~": "",
    "/": "",
    "\\": "",
    "“": "",
    "£": "",
    "@": "",
    "}": "",
    "{": "",
    "^": "",
    "\n": ""
}

OUTPUT_ENCODING = 'utf-8'

CONV = None
COOKIE_VALUE = open('../ai_tools/.cookie').read()

LANGUAGE_TO_DETECT = "vi"
TESSERACT_EXPECTED_LANGUAGE = 'vie'

def main():
    parser = argparse.ArgumentParser(description='Creates an SRT file from a video file that has hardcoded subtitles')
    parser.add_argument('video_file', help='the path to a video file that has hardcoded subtitles')
    parser.add_argument('srt_file', help='where to put the resulting SRT file, will overwrite if it is already there')
    parser.add_argument('frame_srt_file', help='the path to a SRT file containing timestamps ')
    args = parser.parse_args()
    extract_srt(args.video_file, args.srt_file, args.frame_srt_file)

def extract_srt(video_file, srt_file, frame_srt_file="none"):
    video = FileVideoStream(video_file)
    video.stream.set(cv2.CAP_PROP_POS_FRAMES, FIRST_FRAME)

    if video.stream.isOpened() == False:
        print('Error opening video stream or file')
        return

    sys.stdout = FileAndTerminalStream(srt_file)
    convert_frames_to_srt(video, FIRST_FRAME, frame_srt_file)
    sys.stdout = sys.stdout.terminal

    # cv2.destroyAllWindows()
    video.stop()


class FileAndTerminalStream(object):
    def __init__(self, file):
        self.terminal = sys.stdout
        self.srt = open(file, 'w', encoding=OUTPUT_ENCODING)

    def write(self, message):
        self.terminal.write(message)
        self.srt.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        pass


def convert_frames_to_srt(video, first_frame_pos, srt):
    global CONV
    prev_frame_hash = NO_SUBTILE_FRAME_HASH
    frame_number = first_frame_pos
    reader = SubtitleReader()

    video.start()
    reader.start()

    frame = video.read()

    subs = None
    sub_index = FIRST_SUB_INDEX

    # Read the SRT file
    if srt != "none":
        subs = pysrt.open(srt)
        #print(len(subs))

    cache = []
    while frame is not None:
        cropped_frame = frame[SUBTITLE_BOUNDS_TOP:SUBTITLE_BOUNDS_BOTTOM, SUBTITLE_BOUNDS_LEFT:SUBTITLE_BOUNDS_RIGHT]
        monochrome_frame = to_monochrome_subtitle_frame_custom(cropped_frame)

        # Parse the SRT and extract subtitles by timestamps if found
        if subs != None:
            if len(subs) == sub_index:
                break
            if video.stream.get(cv2.CAP_PROP_FPS) <= 0:
                break
            millis = get_millis_for_frame(video, frame_number)
            srt_millis = subs[sub_index].start.ordinal + 50

            #print(millis, srt_millis, frame_number)
            if srt_millis < millis < srt_millis + 300:
                #print(frame_number)
                #print(millis_to_srt_timestamp(millis))
                cv2.imwrite(f"../output/test{sub_index}-{len(cache)}.png", monochrome_frame)
                line = pytesseract.image_to_string(monochrome_frame, lang=TESSERACT_EXPECTED_LANGUAGE, config=TESSERACT_CONFIG)
                line = clean_up_tesseract_output(line)
                cache.append(line)
                subs[sub_index].ntext = line
                #print(subs[sub_index])

                #print()
                if sub_index == FIRST_SUB_INDEX+1 and TEST:
                    sys.exit(0)
                    pass
                #sub_index+=1
            elif srt_millis < millis < srt_millis + 600:
                otext = subs[sub_index].text
                ntext = subs[sub_index].ntext
                subs[sub_index].text = ntext
                print(cache)
                print(subs[sub_index])
                # print(otext)
                print()
                # Try out custom edge gpt for sentence correction
                # TODO: Add context to the movie for better correction
                if len("".join(cache)) > 10 and False:
                    p = prompt.replace("MESSAGE", str(cache))
                    opt = """Use the following english translation for this subtitle as a base of context for the sentence being corrected:\n""" + str(otext)
                    p = p.replace("OPTIONAL", opt)
                    # print(p)
                    out, CONV = edgegpt(p, COOKIE_VALUE, CONV)
                    print(out)
                print()
                sub_index+=1
                cache = []
            frame_number += 1
            frame = video.read()
            continue
        
        # TODO: Update and refactor this
        # TODO: Check for imagehash, sentence length, sentence similarity and connect the timestamps into one long one
        textImage = Image.fromarray(monochrome_frame)
        frame_hash = imagehash.average_hash(textImage, IMAGE_HASH_SIZE)
        # Only use Tesseract if the subtitle changes. This is for performance
        # and also to avoid having single frames of Tesseract mistakes that get
        # entered into the SRT file.
        hash_difference = abs(prev_frame_hash - frame_hash)
        if hash_difference > MAX_HASH_DIFFERENCE_FOR_SAME_SUBTITLE:
            timestamp = get_millis_for_frame(video, frame_number)
            if frame_hash == NO_SUBTILE_FRAME_HASH:
                # no need to use Tesseract when the input is a white rectangle
                change = EmptySubtitleChange(timestamp)
            else:
                change = SubtitleChange(monochrome_frame, timestamp)
            reader.provide_material(change)

        prev_frame_hash = frame_hash
        frame_number += 1
        frame = video.read()


class SubtitleReader:
    def __init__(self):
        self.changes = Queue(maxsize=128)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def update(self):
        subtitle_index = 1
        prev_line = ""
        prev_change_millis = 0 # either the start or the end of a subtitle line

        while True:
            change = self.changes.get()
            line = change.read_subtitle()

            if line == "":
                continue
            
            # TODO: Language detector
            # TODO: Fix and remove gibberish text as well
            # TODO: Save the score to be used later
            score = 0
            try:
                language = detect(line)
                if language != LANGUAGE_TO_DETECT:
                    score += 1
            except:
                pass
            language = detector.detect_language_of(line)
            confidence_values = detector.compute_language_confidence_values(line)
            if not (language and language.iso_code_639_1.name.lower() == LANGUAGE_TO_DETECT and confidence_values[0].value >= 0.54):
                score += 1

            isReliable, textBytesFound, details = cld2.detect(line)
            if not isReliable and details[0][1] != LANGUAGE_TO_DETECT:
                score += 1

            if score > 1:
                continue

            # Check for line similarity
            if prev_line != line:
                if prev_line != '':
                    print_line(
                        index=subtitle_index,
                        start_time=prev_change_millis,
                        end_time=change.timestamp,
                        text=prev_line)
                    subtitle_index += 1
                prev_line = line
                prev_change_millis = change.timestamp

    def provide_material(self, subtitle_change):
        self.changes.put(subtitle_change)


def print_line(index, start_time, end_time, text):
    line_start_time = millis_to_srt_timestamp(start_time)
    line_end_time = millis_to_srt_timestamp(end_time)
    print(index)
    print(line_start_time + ' --> ' + line_end_time)
    print(text)
    print()


class SubtitleChange:
    def __init__(self, frame, timestamp):
        self.frame = frame
        self.timestamp = timestamp

    def read_subtitle(self):
        # TODO: Configure tesseract for better output
        #line = pytesseract.image_to_string(self.frame,lang=TESSERACT_EXPECTED_LANGUAGE, config=TESSERACT_CONFIG)
        line = pytesseract.image_to_string(self.frame,lang=TESSERACT_EXPECTED_LANGUAGE)
        return clean_up_tesseract_output(line)


class EmptySubtitleChange:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def read_subtitle(self):
        return ''


def limit_size(size, max_dimensions):
    (width, height) = size
    (max_width, max_height) = max_dimensions

    if width <= max_width and height <= max_height:
        return size

    if width / height > max_width / max_height:
        return (max_width, int(height * max_width / width))
    else:
        return (int(width * max_height / height), max_height)


def to_monochrome_subtitle_frame_custom(cropped_frame):
    # see https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html for more
    # information
    img = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    # make the image monochrome where only the whitest pixel are kept white
    img = cv2.threshold(img, SUBTITLES_MIN_VALUE, 255, cv2.THRESH_BINARY)[1]

    bounds_width = SUBTITLE_BOUNDS_RIGHT - SUBTITLE_BOUNDS_LEFT
    bounds_height = SUBTITLE_BOUNDS_BOTTOM - SUBTITLE_BOUNDS_TOP
    whitespace_below_y = bounds_height - SUBTITLE_BLANK_SPACE_BELOW
    above_subtitles = numpy.array([[0, 0], [0, SUBTITLE_BLANK_SPACE_ABOVE],
        [bounds_width, SUBTITLE_BLANK_SPACE_ABOVE], [bounds_width, 0]])
    below_subtitles = numpy.array([[0, whitespace_below_y], [0, bounds_height],
    [bounds_width, bounds_height], [bounds_width, whitespace_below_y]])
    # ensure white above and below text. Some blank space is needed for
    # Tesseract
    img = cv2.fillPoly(img, pts=[above_subtitles, below_subtitles], color=0)

    # Add some blur since some pixels within the subtitles are not completely
    # white. This also eliminates smaller groups of white pixels outside of the
    # subtitles
    #img = cv2.GaussianBlur(img, SUBTITLE_IMAGE_BLUR_SIZE, 0)
    img = cv2.threshold(img, SUBTITLES_MIN_VALUE_AFTER_BLUR, 255, cv2.THRESH_BINARY)[1]
    
    # Invert the colors to have white background with black text.
    img = cv2.bitwise_not(img)
    return img

def to_monochrome_subtitle_frame(cropped_frame):
    # see https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html for more
    # information
    img = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    # make the image monochrome where only the whitest pixel are kept white
    img = cv2.threshold(img, SUBTITLES_MIN_VALUE, 255, cv2.THRESH_BINARY)[1]

    bounds_width = SUBTITLE_BOUNDS_RIGHT - SUBTITLE_BOUNDS_LEFT
    bounds_height = SUBTITLE_BOUNDS_BOTTOM - SUBTITLE_BOUNDS_TOP
    whitespace_below_y = bounds_height - SUBTITLE_BLANK_SPACE_BELOW
    above_subtitles = numpy.array([[0, 0], [0, SUBTITLE_BLANK_SPACE_ABOVE], [bounds_width, SUBTITLE_BLANK_SPACE_ABOVE], [bounds_width, 0]])
    below_subtitles = numpy.array([[0, whitespace_below_y], [0, bounds_height],
    [bounds_width, bounds_height], [bounds_width, whitespace_below_y]])
    # ensure white above and below text. Some blank space is needed for
    # Tesseract
    img = cv2.fillPoly(img, pts=[above_subtitles, below_subtitles], color=0)

    # Add some blur since some pixels within the subtitles are not completely
    # white. This also eliminates smaller groups of white pixels outside of the
    # subtitles
    #img = cv2.GaussianBlur(img, SUBTITLE_IMAGE_BLUR_SIZE, 0)
    #img = cv2.threshold(img, SUBTITLES_MIN_VALUE_AFTER_BLUR, 255, cv2.THRESH_BINARY)[1]
    
    # Invert the colors to have white background with black text.
    img = cv2.bitwise_not(img)
    return img


def clean_up_tesseract_output(text):
    for key, value in COMMON_MISTAKES.items():
        text = text.replace(key, value)
    text = text.strip()
    return text


def millis_to_srt_timestamp(total_millis):
    (total_seconds, millis) = divmod(total_millis, 1000)
    (total_minutes, seconds) = divmod(total_seconds, 60)
    (hours, minutes) = divmod(total_minutes, 60)
    time_format = '{:02}:{:02}:{:02},{:03}'
    return time_format.format(int(hours), int(minutes), int(seconds), int(millis))


def get_millis_for_frame(video, frame_number):
    return 1000.0 * frame_number / video.stream.get(cv2.CAP_PROP_FPS)

if __name__ == "__main__":
    main()
