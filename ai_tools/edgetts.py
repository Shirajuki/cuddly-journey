import os

def edgetts(text, voice, output_file):
    payload = f"edge-tts --rate=+5% --voice {voice} --text '{text}' --write-media {output_file}"
    os.popen(payload).read()
