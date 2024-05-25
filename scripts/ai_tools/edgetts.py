import os

def edgetts(text, voice, output_file, rate="+5%"):
    payload = f"edge-tts --rate={rate} --voice {voice} --text '{text}' --write-media {output_file}"
    os.popen(payload).read()
