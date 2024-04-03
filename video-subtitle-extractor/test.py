from imutils.video import FileVideoStream
import cv2
import subprocess
import sys
SUBTITLE_BOUNDS_LEFT = 0
SUBTITLE_BOUNDS_RIGHT = 1280
SUBTITLE_BOUNDS_TOP = 620-50
SUBTITLE_BOUNDS_BOTTOM = 720-20

def get_millis_for_frame(video, frame_number):
    return 1000.0 * frame_number / video.stream.get(cv2.CAP_PROP_FPS)

def millis_to_srt_timestamp(total_millis):
    (total_seconds, millis) = divmod(total_millis, 1000)
    (total_minutes, seconds) = divmod(total_seconds, 60)
    (hours, minutes) = divmod(total_minutes, 60)
    time_format = '{:02}:{:02}:{:02},{:03}'
    return time_format.format(int(hours), int(minutes), int(seconds), int(millis))


video = FileVideoStream("../deathparadevn01.mkv")
video.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)

if video.stream.isOpened() == False:
    print('Error opening video stream or file')
print(video)
video.start()
frame = video.read()

with open("nice.txt") as f:
    a = f.read().split("\n")[:-1]
mss = []
for line in a:
    print(line)
    if not line.startswith("Frame:"):
        continue
    line = line.replace("Frame: ", "")
    h, m, s, ms = line.split('__')[0].split('_')
    total_ms = int(ms) + int(s) * 1000 + int(m) * 60 * 1000 + int(h) * 60 * 60 * 1000
    print(h, m, s)
    print(total_ms)
    mss.append(total_ms)

frame_number = 0
mss = mss[::-1]
srt_millis = mss.pop()
print(srt_millis)
while frame is not None:
    if video.stream.get(cv2.CAP_PROP_FPS) <= 0:
        break
    millis = get_millis_for_frame(video, frame_number)
    if srt_millis - 10 < millis < srt_millis + 10:
        print(frame_number, millis, millis_to_srt_timestamp(millis))
        cropped_frame = frame[SUBTITLE_BOUNDS_TOP:SUBTITLE_BOUNDS_BOTTOM, SUBTITLE_BOUNDS_LEFT:SUBTITLE_BOUNDS_RIGHT]
        # cv2.imwrite(f"./test/{str(frame_number).rjust(10,'0')}.png", cropped_frame)
        if len(mss) > 0:
            srt_millis = mss.pop()
        else:
            srt_millis = 999999999
    frame_number += 1
    frame = video.read()
