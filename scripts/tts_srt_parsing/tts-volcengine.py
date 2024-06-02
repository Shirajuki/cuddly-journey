import os
import sys
import pysrt
import re
import threading

sys.path.append('../ai_tools')
from edgetts import edgetts
sys.path.append('../tts_srt_parsing')

def srt_parse(srt):
    print("[*] Processing SRT...")
    if srt == "none":
        return

    subs = pysrt.open(srt)
    srt_process(subs)

def generate_tts(text, duration, index):
    out = os.path.join(os.path.abspath("../output"), f"{index}.wav")
    text = text.replace("'",'"')
    payload = f"""curl -X POST -s https://translate.volcengine.com/crx/tts/v1/ -H "Content-type: application/json" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" -H "Authority: translate.volcengine.com" -H "Origin: chrome-extension://klgfhbdadaspgppeadghjjemk" -H "Cookie: hasUserBehavior=1" --data-raw '{{"text": "{text}", "speaker": "tts.other.BV074_streaming", "language":"vi"}}' | jq '.audio.data' | python3 -c "print(input()[1:-1])" | base64 -d > {out}"""
    # Generate tts
    os.popen(payload).read()
    print(index, text)

def srt_process(srt_list):
    print("[*] Generating TTS...")
    os.popen(f"echo 0 > ../output/progress-process-tts.txt").read()
    i = 0
    chunk_size = 100
    chunks = [srt_list[i:i + chunk_size] for i in range(0, len(srt_list), chunk_size)]
    for chunk in chunks:
        threads = []
        for sub in chunk:
            thread = threading.Thread(target=generate_tts, args=(sub.text, sub.duration.milliseconds, i))
            threads.append(thread)
            i += 1
    
        # Start all the threads
        for thread in threads:
            thread.start()
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        os.popen(f"echo {int(i/len(srt_list) * 100)} > ../output/progress-process-tts.txt").read()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 tts-edge.py input.srt")
    else:
        print("[*] Parsing...")
        srt_parse(sys.argv[1])
