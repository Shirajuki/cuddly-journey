import os
import sys
import pysrt
import re
import threading
from pydub import AudioSegment
from pydub.effects import speedup
import urllib.parse

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
    out = os.path.join(os.path.abspath("../output"), f"{index}.mp3")
    ntext = urllib.parse.quote_plus(text)
    payload = f"""wget -q "https://dict.youdao.com/dictvoice?audio={ntext}&le=vi" -O {out}"""
    # Generate tts
    os.popen(payload).read()
    print(index, text, flush=True)
    # Get length, shorten audio if speech is slower than intended sub duration
    audio = AudioSegment.from_file(out)
    audio_duration = len(audio)
    # Speedup
    if duration + 350 <= audio_duration:
        final = speedup(audio, playback_speed=1.10)
        final.export(out, format="mp3")

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
