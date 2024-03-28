import os
import sys
import pysrt
import re
import cv2
import json
import threading
from pydub import AudioSegment

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

def get_millis_from_video(video_file):
    payload = f"exiftool {video_file} | grep 'Duration' | head -n1"
    millis = os.popen(payload).read().split(" : ")[-1].strip()
    return srt_timestamp_to_millis(millis)

def get_millis_from_audio(audio_file):
    payload = f"ffprobe -show_entries stream=duration -of compact=p=0:nk=1 -v fatal {audio_file} | tail -n1"
    millis = os.popen(payload).read().strip()
    millis = int(float(millis)*1000)
    return millis

def standalone_parse():
    def parse(f, audios):
        audio = AudioSegment.from_file(f"../output/{f}")
        audio_object = {}
        audio_object["audio"] = audio
        audio_object["duration"] = len(audio)
        audio_object["name"] = f
        audios[int(f.split(".")[0])] = audio_object
        print(len(audios), f)

    audios = {}
    threads = []
    files = os.listdir("../output")
    
    for f in files:
        if (f.endswith(".mp3") or f.endswith(".wav")) and not f.startswith("output"):
            thread = threading.Thread(target=parse, args=(f, audios))
            threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return audios, {}

def standalone_process(data, segments, audios):
    audio_segment = audios[data["index"]]
    audio_segment["start"] = data["start"]

    segments[data["index"]%3].append(audio_segment)

def standalone_save(audios, segments):
    print("[*] Saving audio...")
    # Get max duration from data
    last_audio = audios[max(*audios.keys())]
    
    print("Overlay audios in segments")
    # Create 3 empty audio segments and process through the segments
    audio_segments = [AudioSegment.silent(duration=last_audio["start"]+last_audio["duration"]) for _ in range(len(segments))]
    for i, audio_segment in enumerate(segments):
        print(f"Segment num:", i)
        for seg in audio_segment:
            audio_segments[i] = audio_segments[i].overlay(seg["audio"], position=seg["start"])

    print("Combining audio segments into one track")
    # Overlay all the different audio segments into one
    combined = audio_segments[0].overlay(audio_segments[1])
    for i, seg in enumerate(audio_segments):
        if i > 1:
            combined = combined.overlay(seg)
    file_handle = combined.export("../output/output.mp3", format="mp3")

def srt_parse(srt, data, meta={}):
    segments = [[],[],[]]
    subs = pysrt.open(srt)
    print("[*] Processing...")
    for i in range(len(subs)):
        # start = subs[i].start.ordinal
        start = srt_timestamp_to_millis(str(subs[i].start))
        d = {"index": i, "start": start}
        standalone_process(d, segments, meta)

    standalone_save(data, segments)

if __name__ == "__main__":
    srt =  "../output/subbed.srt"
    if srt == "none":
        exit(0)

    print("[*] Parsing...")
    data, meta = standalone_parse()
    srt_parse(srt, data, data)

