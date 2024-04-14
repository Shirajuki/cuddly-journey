from imutils.video import FileVideoStream
import cv2
import subprocess
import sys
import numpy
import pytesseract

SUBTITLE_BOUNDS_LEFT = 0
SUBTITLE_BOUNDS_RIGHT = 1280
SUBTITLE_BOUNDS_TOP = 620-50
SUBTITLE_BOUNDS_BOTTOM = 720-20

SUBTITLE_BLANK_SPACE_ABOVE = 17
SUBTITLE_BLANK_SPACE_BELOW = 13
SUBTITLES_MIN_VALUE = 200

# After blurring the image we make the image monochrome since that works better
# for Tesseract. This is the limit for what should be considered a (white)
# subtitle pixel after the blur.
SUBTITLES_MIN_VALUE_AFTER_BLUR = 50
TESSERACT_CONFIG = ''
TESSERACT_EXPECTED_LANGUAGE = 'vie'
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
    "\n": " "
}

def get_millis_for_frame(video, frame_number):
    return 1000.0 * frame_number / video.stream.get(cv2.CAP_PROP_FPS)

def millis_to_srt_timestamp(total_millis):
    (total_seconds, millis) = divmod(total_millis, 1000)
    (total_minutes, seconds) = divmod(total_seconds, 60)
    (hours, minutes) = divmod(total_minutes, 60)
    time_format = '{:02}:{:02}:{:02},{:03}'
    return time_format.format(int(hours), int(minutes), int(seconds), int(millis))

def get_contours_by_color(cropped_frame, gray_image):
    image = cropped_frame
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_mask = numpy.zeros_like(gray)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 40 and h > 2 and w > 1:
            cv2.drawContours(contour_mask, [contour], 0, (255), cv2.FILLED)
            # cv2.rectangle(contour_mask, (x, y), (x+w, y+h), (0, 255, 0), 2)
    kernel = numpy.ones((5,5), numpy.uint8) 
    edges = cv2.dilate(contour_mask, kernel, iterations=2)
    nimg = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    nimg[edges != 255] = (255,255,255)
    nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2GRAY)
    return nimg

def get_contours_by_canny(cropped_frame, gray_image):
    img = cropped_frame
    kernel = numpy.ones((5,5), numpy.uint8) 
    gray_image = cv2.threshold(gray_image, SUBTITLES_MIN_VALUE_AFTER_BLUR, 255, cv2.THRESH_BINARY)[1]
    # Perform Canny edge detection on the expanded white areas
    edges = cv2.Canny(gray_image, 100, 200, apertureSize = 3)
    edges = cv2.dilate(edges, kernel, iterations=4)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours=list(filter(lambda cont: cv2.arcLength(cont, False) > 60, contours))
    blank = numpy.zeros((img.shape[0],img.shape[1],3), numpy.uint8)
    cv2.drawContours(blank, contours, -1,(255,255,255),2)

    # Erode the dilated edges to get filled edges
    edges = cv2.dilate(blank, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)
    edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours=list(filter(lambda cont: cv2.arcLength(cont, False) > 60, contours))
    contour_mask = numpy.zeros_like(edges)
    # cv2.drawContours(contour_mask, contours, -1, (255,255,255), 1)
 
    # Get the center of the image
    center_x = img.shape[1] // 2
    center_y = img.shape[0] // 2
    # Loop through contours
    sizes = []
    for contour in contours:
        # Get the bounding rectangle of each contour
        x, y, w, h = cv2.boundingRect(contour)
        bounding_rect_center_x = x + w // 2
        bounding_rect_center_y = y + h // 2
        # Calculate the distance from the center of the image to the center of the bounding rectangle
        distance_x = abs(center_x - bounding_rect_center_x)
        distance_y = abs(center_y - bounding_rect_center_y)
    
        # Define a threshold for how far from the center of the image the bounding rectangle's center can be
        threshold = 50  # Adjust this threshold as needed
        # Check if the bounding rectangle is in the middle
        if distance_x < threshold and distance_y < threshold:
            sizes.append(w*h)
        else:
            sizes.append(0)
    # Fill the bounding rectangle in the mask by size
    while len(sizes) > 0 and max(sizes) != 0:
        i = sizes.index(max(sizes))
        sizes.pop(i)
        cv2.drawContours(contour_mask, [contours.pop(i)], 0, (255), cv2.FILLED)
        # x, y, w, h = cv2.boundingRect(contours.pop(i))
        # cv2.rectangle(contour_mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
        # print(x,y,w,h)
    dilated_contours = cv2.dilate(contour_mask, kernel, iterations=1)
    # Invert the edges to get the areas to keep
    edges = cv2.bitwise_not(dilated_contours)

    nimg = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    # nimg = numpy.copy(gray_image)
    nimg[edges == 255] = (255,255,255)
    nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2GRAY)
    img = nimg
    return img

def to_monochrome_subtitle_frame_custom(cropped_frame):
    img = cropped_frame
    # make the image monochr3me where only the whitest pixel are kept white
    img = cv2.threshold(img, SUBTITLES_MIN_VALUE, 255, cv2.THRESH_BINARY)[1]

    # Draw bounding box rectangles to remove unecessary background colors
    # Ensuring white above and below text. Some blank space is needed for Tesseract
    bounds_width = SUBTITLE_BOUNDS_RIGHT - SUBTITLE_BOUNDS_LEFT
    bounds_height = SUBTITLE_BOUNDS_BOTTOM - SUBTITLE_BOUNDS_TOP
    whitespace_below_y = bounds_height - SUBTITLE_BLANK_SPACE_BELOW
    above_subtitles = numpy.array([[0, 0], [0, SUBTITLE_BLANK_SPACE_ABOVE],
        [bounds_width, SUBTITLE_BLANK_SPACE_ABOVE], [bounds_width, 0]])
    below_subtitles = numpy.array([[0, whitespace_below_y], [0, bounds_height],
    [bounds_width, bounds_height], [bounds_width, whitespace_below_y]])
    img = cv2.fillPoly(img, pts=[above_subtitles, below_subtitles], color=0)
    
    # Invert the colors to have white background with black text.
    img = cv2.bitwise_not(img)
    # Turn image into grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find pixels that are not black or white by a threshold
    img = cv2.threshold(img, SUBTITLES_MIN_VALUE_AFTER_BLUR, 255, cv2.THRESH_BINARY)[1]
    return img

def clean_up_tesseract_output(text):
    for key, value in COMMON_MISTAKES.items():
        text = text.replace(key, value)
    text = text.strip()
    return text

video = FileVideoStream("../deathparadevn01.mkv")
video.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)

if video.stream.isOpened() == False:
    print('Error opening video stream or file')
print(video)
video.start()
frame = video.read()

with open("nice.txt") as f:
    a = f.read().split("\n")[:-1]
mss = []
for line in a:
    print(line)
    if not line.startswith("Frame:"):
        continue
    line = line.replace("Frame: ", "")
    h, m, s, ms = line.split('__')[0].split('_')
    from_total_ms = int(ms) + int(s) * 1000 + int(m) * 60 * 1000 + int(h) * 60 * 60 * 1000
    h, m, s, ms, _ = line.split('__')[1].split('_')
    to_total_ms = int(ms) + int(s) * 1000 + int(m) * 60 * 1000 + int(h) * 60 * 60 * 1000
    print(h, m, s)
    print(from_total_ms)
    print(to_total_ms)
    obj = {"from": from_total_ms, "to": to_total_ms}
    mss.append(obj)

frame_number = 0
mss = mss[::-1]
obj = mss.pop()
srt_millis = obj["from"]
print(srt_millis)
index = 1
while frame is not None:
    if video.stream.get(cv2.CAP_PROP_FPS) <= 0:
        break
    millis = get_millis_for_frame(video, frame_number)
    if srt_millis - 10 < millis < srt_millis + 10:
        lines = []
        print(frame_number, millis, millis_to_srt_timestamp(millis))
        print(index)
        index += 1
        print(f"{millis_to_srt_timestamp(obj['from'])} --> {millis_to_srt_timestamp(obj['to'])}")
        cropped_frame = frame[SUBTITLE_BOUNDS_TOP:SUBTITLE_BOUNDS_BOTTOM, SUBTITLE_BOUNDS_LEFT:SUBTITLE_BOUNDS_RIGHT]
        nframe = to_monochrome_subtitle_frame_custom(cropped_frame)
        line = pytesseract.image_to_string(nframe, lang=TESSERACT_EXPECTED_LANGUAGE, config=TESSERACT_CONFIG)
        line = clean_up_tesseract_output(line)
        lines.append(line)
        nframe = get_contours_by_color(cropped_frame, nframe)
        line = pytesseract.image_to_string(nframe, lang=TESSERACT_EXPECTED_LANGUAGE, config=TESSERACT_CONFIG)
        line = clean_up_tesseract_output(line)
        lines.append(line)
        nframe = get_contours_by_canny(cropped_frame, nframe)
        line = pytesseract.image_to_string(nframe, lang=TESSERACT_EXPECTED_LANGUAGE, config=TESSERACT_CONFIG)
        line = clean_up_tesseract_output(line)
        lines.append(line)
        for l in lines:
            print(l)
        print()
        cv2.imwrite(f"./test/{str(frame_number).rjust(10,'0')}.png", nframe)
        if frame_number > 10000:
            exit()
        if len(mss) > 0:
            obj = mss.pop()
            srt_millis = obj["from"]
        else:
            srt_millis = 999999999
    frame_number += 1
    frame = video.read()
