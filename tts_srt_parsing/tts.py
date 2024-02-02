import os
import sys
import pysrt
import re
import threading

sys.path.append('../ai_tools')
from edgetts import edgetts
sys.path.append('../tts_srt_parsing')


WORDS_TO_REPLACE = [
    ["D", "Đ"]
]
WORDS_TO_REMOVE = [
    "(Xem anime sớm nhất tai VuiGhe.App nhé!)"
]

def srt_parse(srt):
    if srt == "none":
        return

    filtered_srt = []
    dialogue_srt = []
    
    subs = pysrt.open(srt)
    for i in range(len(subs)):
        text = subs[i].text.replace("\n", " ").split()
        text = " ".join(text)

        # Parse thinking dialogues
        ntext = text
        for match in re.findall(r'\(.*\)',text):
            ntext = ntext.replace(match, "")
        if len(ntext.strip()) == 0:
            filtered = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": text}
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
        for wtr in WORDS_TO_REMOVE:
            text = text.replace(wtr, "")

        dialogue = {"timestamp": f"{subs[i].start} --> {subs[i].end}", "text": text}
        dialogue_srt.append(dialogue)

    srt_process(dialogue_srt, "../output/subbed.srt", tts=True)
    srt_process(filtered_srt, "../output/filtered.srt")

def srt_process(srt_list, outfile, tts=False):
    with open(outfile, "w") as f:
        for sub in srt_list:
            f.write(f"{sub['timestamp']}\n{sub['text']}\n\n")

    if tts:
        threads = []
        for i, sub in enumerate(srt_list):
            out = os.path.join(os.path.abspath("../output"), f"{i}.mp3")
            thread = threading.Thread(target=edgetts, args=(sub["text"], out))
            threads.append(thread)
        
        # Start all the threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    srt_parse("ep1.txt")

    

