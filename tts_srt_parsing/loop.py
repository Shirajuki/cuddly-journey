import os
for i in range(1,25):
    i = str(i).rjust(2, "0")
    payload = f"python3 process_srt.py ../apoth/Kusuriya\ no\ Hitorigoto\ -\ {i}.srt False False && cp ../output/subbed.srt ep{i}.srt && cp ../output/filtered.srt filter{i}.srt"
    print(payload)
    os.system(payload)
    payload = f"python3 tts-edge.py ep{i}.srt && powershell.exe -c '[console]::beep(500,300)'; python3 ../process_video/standalone.py && cp ../output/output.mp3 ep{i}.mp3 && powershell.exe -c '[console]::beep(500,300)'"
    print(payload)
    os.system(payload)
    os.system("rm -rf ../output/*.mp3")
    os.system("rm -rf ../output/*.srt")


