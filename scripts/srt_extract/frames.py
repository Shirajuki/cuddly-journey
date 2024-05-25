import pysrt

def millis_to_srt_timestamp(total_millis):
    (total_seconds, millis) = divmod(total_millis, 1000)
    (total_minutes, seconds) = divmod(total_seconds, 60)
    (hours, minutes) = divmod(total_minutes, 60)
    time_format = '{:02}:{:02}:{:02},{:03}'
    return time_format.format(int(hours), int(minutes), int(seconds), int(millis))

def get_millis_for_frame(video, frame_number):
    return 1000.0 * frame_number / video.stream.get(cv2.CAP_PROP_FPS)

subs = pysrt.open('crossroad.srt')
print(len(subs))
for sub in subs:
    millis = sub.start.ordinal + 400
    print(millis, millis_to_srt_timestamp(millis))
    sub.text = "text"
    print(sub)

