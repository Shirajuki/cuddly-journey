# [WIP] Hardcoded Subtitles to SRT

Creates an [SRT](https://www.matroska.org/technical/subtitles.html#srt-subtitles) file from
a video file that has hardcoded subtitles.

The script relies on [Tesseract](https://github.com/tesseract-ocr/tesseract) for the optical character recognition.

## Features (TODOs)

- Parse SRT-file (either in another language / same language) and extract hardcoded subtitles in given timestamps (Fast)
- Search for and extract the hardcoded subtitles by going through the frames and calculating the timestamps (Slower)
- Web-based GUI editor for easier configuration and semi-automatic corrections
  - Configure total frames to extract from
  - Configure the subtitle crop-box position by specific frames
  - LLM API used for sentence correction
- Process SRT-file and generate audio dubbing through a given TTS model
- All in one tool for easier video subbing and dubbing

## Dependencies

- [Python 3](https://www.python.org/downloads/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract#installing-tesseract) with support for your target language
- [FFmpeg](https://ffmpeg.org/download.html) to convert video to a supported format

To download the required python package dependencies, run

```
pip3 install -r requirements.txt
```

## How to use
To extract sub channels from a video file run:
- ffmpeg -i movie.mkv -map 0:s:0 subs.srt

To extract hardcoded subtitles from a video file run:
- `ffmpeg -i input.mp4 -vcodec copy -acodec copy movie.mkv` (may be different depending on the video format)
- `python3 hard_subs_to_srt.py movie.mkv output.srt crossroad.srt`

To generate tts from srt files run:
- `python3 tts.py input.srt`

To process the generated tts into an audio file:
- `python3 standalone.py`

Note that the script currently only support HD (1280x720) videos for now

# Credits

- [victorjoh](https://github.com/victorjoh/hard-subs-to-srt) for the initial code that this project were based on
- [rany2](https://github.com/rany2/edge-tts) for the Microsoft Edge's tts python wrapper
- [vsakkas](https://github.com/vsakkas/sydney.py) used as inspiration in reverse engineering the Bing Chat / Copilot / Sydney API
