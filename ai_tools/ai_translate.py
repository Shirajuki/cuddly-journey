import sys
import pysrt
import math
import time
from deep_translator import GoogleTranslator
from edgegpt import edgegpt

FROM_LANG = "en"
LANG = "vi"
LANGUAGE = "Vietnamese"
PROMPT = """
You are a professional translator. Your task is to translate all the following sentences from their original language into LANGUAGE. Each sentence is given a unique id number and is listed one by one. Translate each sentence without missing any and return the translated sentences with their corresponding id numbers on a new line. The format is as follows: '[id]. [translated text]'. Please note that only the translated text is needed and only list out the answer, phonetic annotation is not required. Start your answer with START when listing the translations and end with END. Also write the translated text in their own lines. Only give me the answer and do not say anything else unnecessary.

PARSED_SRT
"""

COOKIE_VALUE = open('.cookie').read()

def srt_parse(srt):
    print("[*] Processing SRT...")
    if srt == "none":
        return

    srt_list = []
    subs = pysrt.open(srt)
    for i in range(len(subs)):
        srt_obj = f"{i+1}. {subs[i].text}"
        srt_list.append(srt_obj)
    srt_process(subs, srt_list)

def batch_process(srt_list):
    # Split and process srt list into batches
    conv = None
    batch_count = math.ceil(len("\n".join(srt_list)) / 2000)+1
    print(batch_count, len("\n".join(srt_list)) / 2000)
    skip = len(srt_list)//batch_count
    batch = [srt_list[i:i+skip] for i in range(0,len(srt_list),skip)]
    outs = []
    for i in range(len(batch)):
        prompt = PROMPT.replace("LANGUAGE", LANGUAGE)
        prompt = prompt.replace("PARSED_SRT", "\n".join(batch[i]))
        out, conv = edgegpt(prompt, COOKIE_VALUE, conv)
        outs.append(out)
        time.sleep(5)
    return outs

def srt_process(subs, srt_list):
    print("[*] Translating SRT...")
    # Parse batches into one and update subs with translated text
    outs = batch_process(srt_list)
    out = "\n".join(outs)
    outs = out.split("\n")
    subs_output = ""
    changes = {}
    for i in range(len(outs)):
        try:
            num, text =  int(outs[i].split()[0][:-1]), outs[i].split()[1:]
            subs[num-1].text = " ".join(text).strip()
            changes[num-1] = True
        except:
            pass

    # Recheck if there was any place with failed translations and retry
    runs = 4
    for j in range(runs):
        retries = []
        for i in range(len(srt_list)):
            if changes.get(i, False):
                continue
            retries.append(srt_list[i])
        if len(retries) == 0:
            break
        
        # Translate text using google translate on last run if the past runs fails
        if j == runs-1:
            for i in range(len(retries)):
                num, text =  int(retries[i].split()[0][:-1]), retries[i].split()[1:]
                text = " ".join(text).strip()
                translated = GoogleTranslator(source=FROM_LANG, target=LANG).translate(text=text)
                subs[num-1].text = translated
                changes[num-1] = True
            break

        # Parse batches into one and update subs with translated text
        outs = batch_process(retries)
        out = "\n".join(outs)
        outs = out.split("\n")
        subs_output = ""
        for i in range(len(outs)):
            try:
                num, text =  int(outs[i].split()[0][:-1]), outs[i].split()[1:]
                subs[num-1].text = " ".join(text).strip()
                changes[num-1] = True
            except:
                pass

    print(len(changes), len(subs), len(changes) == len(subs))
    # Write SRT to file
    for i in range(len(subs)):
        subs_output += str(subs[i])+"\n"
    with open('../output/translated.srt', 'w') as f:
        f.write(subs_output)
    print(subs_output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 ai_translate.py input.srt")
    else:
        print("[*] Parsing...")
        srt_parse(sys.argv[1])


