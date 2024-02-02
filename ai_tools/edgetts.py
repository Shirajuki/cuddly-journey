import os
# import edge_tts

VOICE = "en-GB-SoniaNeural"

def edgetts(text, output_file):
    payload = f"edge-tts --rate=+5% --voice vi-VN-HoaiMyNeural --text '{text}' --write-media {output_file}"
    os.popen(payload).read()
