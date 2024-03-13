import os
import sys
import pysrt
import re
import threading
from pydub import AudioSegment

sys.path.append('../ai_tools')
from edgetts import edgetts
sys.path.append('../tts_srt_parsing')

WORDS_TO_REPLACE = [
    ["D", "Đ"],
]
CHARACTERS_TO_REPLACE = [
    ["“", '"'],
    ["”", '"'],
]
TEXT_TO_REMOVE = [
    "(Xem anime sớm nhất tai VuiGhe.App nhé!)",
    "(Xem anime sớm nhất tạii VuiGhe.App nhé!)"
]

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

def srt_parse(srt):
    print("[*] Processing SRT...")
    if srt == "none":
        return

    filtered_srt = []
    dialogue_srt = []
    
    subs = pysrt.open(srt)
    for i in range(len(subs)):
        # Parse multiple dialogues on same timestamp
        texts = [x.strip() for x in subs[i].text.split("\n-")]
        if len(texts) > 1:
            texts = [" ".join(x.replace("\n", " ").split()) for x in texts]
            texts = [x[1:].strip() if x.startswith("-") else x.strip() for x in texts]
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

            # Remove words
            for ttr in TEXT_TO_REMOVE:
                text = text.replace(ttr, "")

            # Parse display text and thinking dialogues
            ntext = text
            filtered_texts = []
            for match in re.findall(r'\(.*\)',text):
                ntext = ntext.replace(match, "")
                filtered_texts.append(f"{match}")
            if len(filtered_texts) > 0:
                filtered = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": " ".join(filtered_texts), "duration": subs[i].duration}
                filtered_srt.append(filtered)
            if len(ntext.strip()) == 0:
                continue

            dialogue = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": ntext.strip(), "duration": subs[i].duration}
            dialogue_srt.append(dialogue)

    # Merge dialogues if duplicate
    ndialogue_srt = []
    for i, dialogue in enumerate(dialogue_srt):
        # Skip dialogue if the skip value is set
        if dialogue.get("skip", False):
            continue
        # Seek 4 next dialogues and merge them if text is same
        next = dialogue_srt[i+1:i+5]
        if len(next) == 0:
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

    srt_process(ndialogue_srt, "../output/subbed.srt", tts=True)
    srt_process(filtered_srt, "../output/filtered.srt")

def generate_tts(text, duration, index):
    out = os.path.join(os.path.abspath("../output"), f"{index}.mp3")
    voice = "vi-VN-HoaiMyNeural"
    # Generate tts
    edgetts(text, voice, out)
    # Get length, shorten audio if speech is slower than intended sub duration
    audio = AudioSegment.from_file(out)
    audio_duration = len(audio)
    duration = srt_timestamp_to_millis(str(duration))
    # Speedup
    if duration + 350 <= audio_duration:
        edgetts(text, voice, out, "+40%")

def srt_process(srt_list, outfile, tts=False):
    print("[*] Generating TTS...")
    with open(outfile, "w") as f:
        for i, sub in enumerate(srt_list):
            f.write(f"{i+1}\n{sub['timestamp']}\n{sub['text']}\n\n")

    if tts:
        threads = []
        for i, sub in enumerate(srt_list):
            thread = threading.Thread(target=generate_tts, args=(sub["text"], sub["duration"], i))
            threads.append(thread)
        
        # Start all the threads
        for thread in threads:
            thread.start()
        # Wait for all threads to complete
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 tts.py input.srt")
    else:
        print("[*] Parsing...")
        srt_parse(sys.argv[1])
