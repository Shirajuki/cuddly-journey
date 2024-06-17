import sys

def srt_timestamp_to_millis(timestamp):
    if "." in timestamp:
        time_format, millis = timestamp.split(".")
    else:
        time_format = timestamp
        millis = "0"
    time_format = time_format.split(":")
    millis = int(millis)
    millis += int(time_format[-1]) * 1000
    millis += int(time_format[-2]) * 60*1000
    millis += int(time_format[-3]) * 60*60*1000
    return millis

def millis_to_srt_timestamp(total_millis):
    (total_seconds, millis) = divmod(total_millis, 1000)
    (total_minutes, seconds) = divmod(total_seconds, 60)
    (hours, minutes) = divmod(total_minutes, 60)
    time_format = '{:02}:{:02}:{:02},{:03}'
    return time_format.format(int(hours), int(minutes), int(seconds), int(millis))

def ass_parse(inp, outp):
    with open(inp) as f:
        ass = f.readlines()

    subs = []
    p = False
    for line in ass:
        if "[Events]" in line:
            p = True
            continue
        if p:
            if "Default" in line:
                meta = line.split(",")[:9]
                text = " ".join(line.split(",")[9:]).strip()
                dtype = meta[0]
                if "Comment" in dtype:
                    if any([text.startswith(x) for x in '"\'[(']):
                        if not text.startswith("["):
                            text = f"[ {text} ]"
                text = text.replace("\\N", "")

                # Remove format on texts {\\X}
                ind = text.find("{\\")
                while ind >= 0:
                    ind2 = text.find("}")
                    part = text[ind:ind2]
                    text = text.replace(part, "")
                    ind = text.find("{\\")
                text = text.strip()

                start = srt_timestamp_to_millis(meta[1])
                end = srt_timestamp_to_millis(meta[2])
                sub = {"text": text, "start": start, "end": end}
                subs.append(sub)

    output = []
    subs = sorted(subs, key=lambda s: s['start'])
    for i, sub in enumerate(subs):
        start = millis_to_srt_timestamp(sub["start"])
        end = millis_to_srt_timestamp(sub["end"])
        out = f"{i}\n{start} --> {end}\n{sub['text']}"
        output.append(out)
    output = "\n\n".join(output)
    print(output)
    
    with open(outp, "w") as f:
        f.write(output)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 ass_to_srt.py input.ass output.srt")
    else:
        print("[*] Parsing...")
        ass_parse(sys.argv[1], sys.argv[2])
