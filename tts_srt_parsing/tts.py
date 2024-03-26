import os
import sys
import pysrt
import re
import threading
from pydub import AudioSegment

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
    voice = "vi-VN-HoaiMyNeural"
    # Generate tts
    edgetts(text, voice, out)
    # Get length, shorten audio if speech is slower than intended sub duration
    audio = AudioSegment.from_file(out)
    audio_duration = len(audio)
    # Speedup
    if duration + 350 <= audio_duration:
        edgetts(text, voice, out, "+10%")

def srt_process(srt_list):
    print("[*] Generating TTS...")
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 tts.py input.srt")
    else:
        print("[*] Parsing...")
        srt_parse(sys.argv[1])
