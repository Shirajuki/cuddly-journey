import os
import sys
import pysrt
import re
import time

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

def process_srt(srt, input_video=""):
    if srt == "none" or input_video == "":
        return

    subs = pysrt.open(srt)
    for i in range(0, len(subs)):
        start = srt_timestamp_to_millis(str(subs[i].start))/1000
        duration = srt_timestamp_to_millis(str(subs[i].duration))/1000
        payload = f"ffmpeg -i {input_video} -ss {start} -t {duration} ../output/extract{i}.mp3 -n"
        print(payload)
        os.popen(payload)
        if i%8 == 0:
            time.sleep(24)
    time.sleep(24)

def classify_gender(audio_file):
    payload = f"ina_speech_segmenter.py -i {audio_file} -o ../output -g true"
    print(payload)
    os.popen(payload)

def process_speech_segment(srt):
    if srt == "none":
        return

    subs = pysrt.open(srt)
    j = 0
    for i in range(len(subs)):
        audio_file = f"../output/extract{i}.mp3"
        if not os.path.exists(audio_file) or "male" in os.popen(f"cat {audio_file[:-3]+'csv'}").read():
            continue
        classify_gender(audio_file)
        j+=1
        if j%8 == 0 and j>0:
            time.sleep(24)
    time.sleep(24)


if __name__ == "__main__":
    srt = "../output/subbed.srt"
    input_video = "/mnt/c/Users/phucj/Downloads/solo-leveling-01.mkv"
    #print("processing srt...")
    #process_srt(srt)
    print("processing speech segmenter...")
    process_speech_segment(srt, input_video)

