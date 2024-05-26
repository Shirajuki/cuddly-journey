import os


beep = "powershell.exe -c '[console]::beep(500,300)'"
def alert(text):
    return f"""powershell.exe -c 'Add-Type -AssemblyName System.speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{text}")'"""

for i in range(1,25):
    i = str(i).rjust(2, "0")
    payload = f"python3 ./tts_srt_parsing/process_srt.py ./apoth/Kusuriya\ no\ Hitorigoto\ -\ {i}.srt False False && cp ./scripts/output/subbed.srt ep{i}.srt && cp ./scripts/output/filtered.srt ep{i}_filter.srt"
    print(payload)
    os.system(payload)
    payload = f"python3 ./scripts/tts_srt_parsing/tts-edge.py ep{i}.srt && {beep}; python3 ./scripts/process_video/standalone.py && cp ./scripts/output/output.mp3 ep{i}.mp3 && {beep}; {alert(f'ep{i}')}"
    print(payload)
    os.system(payload)
    os.system("rm -rf ./scripts/output/*.mp3")
    os.system("rm -rf ./scripts/output/*.srt")


