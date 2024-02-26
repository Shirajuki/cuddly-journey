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
    ["D", "Đ"]
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
        
        # Parse thinking dialogues
        for text in texts:
            ntext = text
            for match in re.findall(r'\(.*\)',text):
                ntext = ntext.replace(match, "")
            if len(ntext.strip()) == 0:
                filtered = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": text, "duration": subs[i].duration}
                filtered_srt.append(filtered)
                continue

            # Replace words
            text = text.split()
            for wtr in WORDS_TO_REPLACE:
                for j, word in enumerate(text):
                    if word in [wtr[0], wtr[0]+",", wtr[0]+"!", wtr[0]+"."]:
                        text[j] = word.replace(wtr[0], wtr[1])
            text = " ".join(text)

            # Remove words
            for ttr in TEXT_TO_REMOVE:
                text = text.replace(ttr, "")

            dialogue = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": text, "duration": subs[i].duration}
            dialogue_srt.append(dialogue)

    srt_process(dialogue_srt, "../output/subbed.srt", tts=True)
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
