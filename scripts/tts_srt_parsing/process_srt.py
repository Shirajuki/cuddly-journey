import os
import sys
import pysrt
import re
import threading
from pydub import AudioSegment
from lingua import Language, LanguageDetectorBuilder
from langdetect import detect
import pycld2 as cld2

sys.path.append('../ai_tools')
from edgetts import edgetts
sys.path.append('../tts_srt_parsing')

languages = [Language.VIETNAMESE, Language.JAPANESE]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

LANGUAGE_TO_DETECT = "vi"
CHARACTERS_TO_REPLACE = [
    ["“", '"'],
    ["”", '"'],
    ["'", ""],
]
WORDS_TO_REPLACE = [
    ["D", "Đ"],
]
SENTENCE_TO_REPLACE = [
    ['<font face="Gandhi Sans" size="75">', ''],
    ['<font ', ''],
    ['</font>', ''],
    ['<i>', ''],
    ['</i>', ''],
    ['{\\an8}', ''],
    ['…','...'],
    ["(Xem anime sớm nhất tai VuiGhe.App nhé!)", ""],
    ["(Xem anime sớm nhất tạii VuiGhe.App nhé!)", ""]
]
REGEX = r'((size=("30")+(.*)<\/font>)|(face=("(OranienbaumEroded||Cagliostro||Courte||BorisBlackBloxx||Kozuka Mincho Pro Strippedv2 R||FOT Seurat ProN Strp Medium)"))+(.*)<\/font>)'

def srt_timestamp_to_millis(timestamp):
    if "," in timestamp:
        time_format, millis = timestamp.split(",")
    else:
        time_format = timestamp
        millis = "0"
    time_format = time_format.split(":")
    millis = int(millis)
    millis += int(time_format[-1]) * 1000
    millis += int(time_format[-2]) * 60*1000
    millis += int(time_format[-3]) * 60*60*1000
    return millis

def millis_to_srt_timestamp(total_millis):
    (total_seconds, millis) = divmod(total_millis, 1000)
    (total_minutes, seconds) = divmod(total_seconds, 60)
    (hours, minutes) = divmod(total_minutes, 60)
    time_format = '{:02}:{:02}:{:02},{:03}'
    return time_format.format(int(hours), int(minutes), int(seconds), int(millis))

def srt_parse(srt, diff=False, merge=False, crosstalk=False):
    print("[*] Processing SRT...")
    os.popen(f"echo 0 > ../output/progress-process-srt.txt").read()
    if srt == "none":
        return

    filtered_srt = []
    dialogue_srt = []
    
    subs = pysrt.open(srt)
    for i in range(len(subs)):
        # Parse multiple dialogues on same timestamp by "-" char / crosstalk
        texts = [x.strip() for x in subs[i].text.split("\n-")]
        if len(texts) > 1:
            texts = [" ".join(x.replace("\n", " ").split()) for x in texts]
            texts = [x[1:].strip() if x.startswith("-") else x.strip() for x in texts]
            if not crosstalk:
                texts = [". ".join(texts)]
        else:
            texts = subs[i].text.replace("\n", " ").split()
            texts = [" ".join(texts)]
        
        # Parse dialogues
        for text in texts:
            # Replace words
            text = text.split()
            for wtr in WORDS_TO_REPLACE:
                for j, word in enumerate(text):
                    if word in [wtr[0], wtr[0]+",", wtr[0]+"!", wtr[0]+"."]:
                        text[j] = word.replace(wtr[0], wtr[1])
            text = " ".join(text)

            # Replace characters
            text = list(text)
            for c in CHARACTERS_TO_REPLACE:
                for j, char in enumerate(text):
                    if char == c[0]:
                        text[j] = c[1]
            text = "".join(text)

            # Parse display text and thinking dialogues
            ntext = text
            filtered_texts = []
            for match in re.findall(REGEX,text):
                if type(match) != str:
                    match = match[0]
                ntext = ntext.replace(match, "")
                filtered_texts.append(f"{match}")

            # Replace sentences
            for stor in SENTENCE_TO_REPLACE:
                ntext = ntext.replace(stor[0], stor[1])

            # Filter if all character is upper
            upper = [x.isupper() for x in ntext if x not in " -:;!?'\".,1234567890"]
            if all(upper) and len(upper) > 2:
                filtered_texts.append(ntext)
                ntext = ""

            if len(filtered_texts) > 0:
                filtered = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": " ".join(filtered_texts), "duration": subs[i].duration}
                filtered_srt.append(filtered)
            if len(ntext.strip()) == 0:
                continue

            dialogue = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": ntext.strip(), "duration": subs[i].duration}
            dialogue_srt.append(dialogue)
    os.popen(f"echo 25 > ../output/progress-process-srt.txt").read()

    # Skip over wrong language subs
    ndialogue_srt = []
    for i, dialogue in enumerate(dialogue_srt):
        if not diff:
            ndialogue_srt.append(dialogue)
            continue
        line = dialogue["text"]
        score = 0
        language = "un"
        try:
            language = detect(line)
            if language == LANGUAGE_TO_DETECT:
                score += 1
        except:
            pass
        language2 = detector.detect_language_of(line)
        confidence_values = detector.compute_language_confidence_values(line)
        if language2 == Language.VIETNAMESE:
            score += 1
        isReliable, textBytesFound, details = cld2.detect(line)

        details = [x[1] for x in details if x[1] != "un"]
        if LANGUAGE_TO_DETECT in details:
            score += 1
        if len(line.split()) == 1:
            score += 1
        if score < 2:
            print('[SKIPPED]', i, score, line)
            continue
        ndialogue_srt.append(dialogue)
    dialogue_srt = ndialogue_srt
    os.popen(f"echo 50 > ../output/progress-process-srt.txt").read()

    # Merge dialogues if duplicate
    ndialogue_srt = []
    for i, dialogue in enumerate(dialogue_srt):
        if not merge:
            ndialogue_srt.append(dialogue)
            continue

        # Skip dialogue if the skip value is set
        if dialogue.get("skip", False):
            continue

        # Seek 4 next dialogues and merge them if text is same
        next = dialogue_srt[i+1:i+5]
        if len(next) == 0:
            ndialogue_srt.append(dialogue)
            continue
        start, end = [srt_timestamp_to_millis(timestamp) for timestamp in dialogue["timestamp"].split(" --> ")]
        duration = srt_timestamp_to_millis(str(dialogue["duration"]))
        for d in next:
            if dialogue["text"] != d["text"]:
                continue
            ds, de = [srt_timestamp_to_millis(t) for t in d["timestamp"].split(" --> ")]
            dd = srt_timestamp_to_millis(str(d["duration"]))
            end = de
            duration += dd
            d["skip"] = True
        dialogue["timestamp"] = f"{millis_to_srt_timestamp(start)} --> {millis_to_srt_timestamp(end)}"
        dialogue["duration"] = millis_to_srt_timestamp(duration)
        ndialogue_srt.append(dialogue)
    os.popen(f"echo 75 > ../output/progress-process-srt.txt").read()

    print("[*] Saving SRT...")
    srt_process(ndialogue_srt, "../output/subbed.srt")
    srt_process(filtered_srt, "../output/filtered.srt")

def srt_process(srt_list, outfile, tts=False):
    with open(outfile, "w") as f:
        for i, sub in enumerate(srt_list):
            f.write(f"{i+1}\n{sub['timestamp']}\n{sub['text']}\n\n")
    os.popen(f"echo 100 > ../output/progress-process-srt.txt").read()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("usage: python3 process_srt.py input.srt [langdiff:True/False] [merge:True/False] [crosstalk:True/False]")
    else:
        print("[*] Parsing...")
        srt_parse(sys.argv[1], sys.argv[2]=="True", sys.argv[3]=="True", sys.argv[4]=="True")
