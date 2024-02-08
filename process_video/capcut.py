import os
import sys
import pysrt
import re
import cv2
import json
import threading

AUDIO_FORMAT = {
"app_id": 0,"category_id": "","category_name": "local","check_flag": 1,"effect_id": "","formula_id": "","intensifies_path": "","is_ai_clone_tone": False,"is_ugc": False,"query": "","request_id": "","resource_id": "","search_id": "","source_platform": 0,"team_id": "","text_id": "","tone_category_id": "","tone_category_name": "","tone_effect_id": "","tone_effect_name": "","tone_second_category_id": "","tone_second_category_name": "","tone_speaker": "","tone_type": "","type": "extract_music","video_id": "","wave_points": [],
"duration": 3666666,
"id": "24F5A166-70BC-4c90-BB69-7693D0A9AC8B",
"name": "0.mp3",
"path": "//wsl.localhost/Ubuntu/home/juki/github/cuddly-journey/output/0.mp3",
}
AUDIO_SEGMENT = {
"cartoon": False,"clip": "null","common_keyframes": [],"enable_adjust": False,"enable_color_curves": True,"enable_color_match_adjust": False,"enable_color_wheels": True,"enable_lut": False,"enable_smart_color_adjust": False,"group_id": "","hdr_settings": "null","intensifies_audio": False,"is_placeholder": False,"is_tone_modify": False,"keyframe_refs": [],"last_nonzero_volume": 1.0,"render_index": 0,"reverse": False,"speed": 1.0,"template_id": "","template_scene": "default","track_attribute": 0,"track_render_index": 0,"uniform_scale": "null","visible": True,
"responsive_layout": {
    "enable": False,
    "horizontal_pos_layout": 0,
    "size_layout": 0,
    "target_follow": "",
    "vertical_pos_layout": 0
},
"id": "4EA1ACED-51E8-4607-80F2-67F29F09BC90",
"material_id": "24F5A166-70BC-4c90-BB69-7693D0A9AC8B",
"source_timerange": {
    "duration": 3666666, "start": 0
},
"target_timerange": {
    "duration": 3666666, "start": 9800000
},
"volume": 1.0
}

def generate_id():
    p1 = os.urandom(4).hex().upper()
    p2 = os.urandom(2).hex().upper()
    p3 = os.urandom(2).hex().upper()
    p4 = os.urandom(2).hex().upper()
    p5 = os.urandom(6).hex().upper()
    return f"{p1}-{p2}-{p3}-{p4}-{p5}"

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

def capcut_parse():
    def parse(f, audios, ids):
        audio_object = AUDIO_FORMAT.copy()
        audio_object["id"] = generate_id()
        audio_object["duration"] = get_millis_from_audio(f"../output/{f}")*1000
        audio_object["name"] = f 
        audio_object["path"] = f"//wsl.localhost/Ubuntu/home/juki/github/cuddly-journey/output/{f}"
        ids[int(f.split(".")[0])] = [audio_object["id"], audio_object["duration"]]
        audios.append(audio_object)
        print(len(audios), f)

    with open("draft_content.json") as f:
        capcut = json.loads(f.read())
    audios = []
    ids = {}
    threads = []
    files = os.listdir("../output")
    for f in files:
        if f.endswith(".mp3"):
            thread = threading.Thread(target=parse, args=(f, audios, ids))
            threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    capcut["materials"]["audios"] = audios
    return capcut, ids

# TODO: Update segments to 3 instead of 2
def capcut_process(data, segments, ids):
    audio_segment = json.loads(json.dumps(AUDIO_SEGMENT))
    audio_segment["id"] = generate_id()
    audio_segment["material_id"] = ids[data["index"]][0]
    audio_segment["source_timerange"] = {"duration": ids[data["index"]][1], "start": 0}
    audio_segment["target_timerange"] = {"duration": ids[data["index"]][1], "start": data["start"]}
    if data["index"]%2 == 0:
        segments[0].append(audio_segment)
    else:
        segments[1].append(audio_segment)

def capcut_save(data, segments):
    print("[*] Saving...")
    # Update video name
    name = "solo-leveling-01.mkv"
    path = f"C:/Users/phucj/Downloads/{name}"
    duration = get_millis_from_video(f"/mnt/c/Users/phucj/Downloads/{name}")*1000
    data["materials"]["videos"][0]["name"] = name
    data["materials"]["videos"][0]["path"] = path
    data["materials"]["videos"][0]["duration"] = duration
    data["tracks"][0]["segments"][0]["source_timerange"]["duration"] = duration
    data["tracks"][0]["segments"][0]["target_timerange"]["duration"] = duration
    data["tracks"][0]["segments"][0]["volume"] = 0.2818382978439331

    # Update audio segments
    data["tracks"][1]["segments"] = segments[0]
    data["tracks"][2]["segments"] = segments[1]
    with open("ndraft_content.json", "w") as f:
        f.write(json.dumps(data))

def srt_parse(srt, data, meta={}):
    segments = [[],[]]
    subs = pysrt.open(srt)
    print("[*] Processing...")
    for i in range(len(subs)):
        start = srt_timestamp_to_millis(str(subs[i].start))*1000
        d = {"index": i, "start": start}
        capcut_process(d, segments, meta)

    capcut_save(data, segments)

if __name__ == "__main__":
    srt =  "../output/subbed.srt"
    if srt == "none":
        exit(0)

    print("[*] Parsing...")
    data, ids = capcut_parse()
    srt_parse(srt, data, ids)
