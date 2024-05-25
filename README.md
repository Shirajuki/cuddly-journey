# [WIP] Hardcoded Subtitles to SRT

An all-in-one tool for video subbing and dubbing. Done by creating an [SRT](https://www.matroska.org/technical/subtitles.html#srt-subtitles) file from
a given video file that has hardcoded subtitles, finally generating an audio dub on the extracted subtitle.

The scripts relies on [Tesseract](https://github.com/tesseract-ocr/tesseract) for the optical character recognition, and FFmpeg for parsing and converting audio/video files.

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

## Useful commands
To convert mkv to mp4 run:
- ffmpeg -i video.mkv -codec copy video.mp4

To convert mp3 to wav run:
- ffmpeg -i audio.mp3 -acodec pcm_u8 -ar 22050 audio.wav

To convert mp4 to mkv run:
- `ffmpeg -i input.mp4 -vcodec copy -acodec copy movie.mkv`

To extract sub channels from a video file run:
- ffmpeg -i movie.mkv -map 0:s:0 subs.srt

## Standalone scripts
To extract hardcoded subtitles from a video file run:
- `python3 ./srt_extract/hard_subs_to_srt.py movie.mkv output.srt helper.srt`

To process and cleanup srt files run (outputs subbed.srt + filtered.srt):
- `python3 ./tts_srt_parsing/process_tts.py input.srt`

To generate tts from srt files run (outputs small tts chunks):
- `python3 ./tts_srt_parsing/tts-edge.py input.srt`

To process the generated tts into an audio file ():
- `python3 ./process_video/standalone.py`

Note that the script currently only support HD (1280x720) videos for now

## How to use
TBA

## Development
TBA

## Docker
TBA

# Credits

The codebase builds upon the foundations of the following projects:

- [victorjoh](https://github.com/victorjoh/hard-subs-to-srt) for the initial code that this project were based on
- [rany2](https://github.com/rany2/edge-tts) for the Microsoft Edge's tts python wrapper
- [vsakkas](https://github.com/vsakkas/sydney.py) used as inspiration in reverse engineering the Bing Chat / Copilot / Sydney API
- [video-subtitle-extractor](https://github.com/YaoFANGUK/video-subtitle-extractor) for the VideoSubFinderCli binary :pray:
