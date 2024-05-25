import sys
import pysrt
import math
import json
import time
from deep_translator import GoogleTranslator
from edgegpt import edgegpt

FALLBACK_LANGUAGE = "english"
LANGUAGE = "vietnamese"
PROMPT = """
Here is a list of parsed LANGUAGE subtitle texts:
PARSED_TEXT

Can you help me clean it up and from all the outputs guess what the correct message is? If you believe something is an abbrevation or doesn't fit in the message please do not include it. If you believe the parsed message came out bad and doesn't include anything meaningful, then write the answer as an empty space. Write your answer in the following format, take for example if the answer is "ANSWER":

START
ID1. ANSWER1
ID2. ANSWER2
END

After that, use the following FALLBACK_LANGUAGE text as a base of fallback for all the empty spaces. Remember translate them to LANGUAGE before answering:
FALLBACK_TEXT

Do not write your thoughts, only give the answer. Make sure there is no answers with only empty spaces. Strip unnecessary special characters at the start and end for each line.
"""
COOKIE_VALUE = open('.cookie').read()

def srt_parse(fallback, parsed):
    print("[*] Parsing SRT...")
    fallback_list = []
    subs = pysrt.open(fallback)
    for i in range(len(subs)):
        srt_obj = f"{i+1}. {subs[i].text}"
        fallback_list.append(srt_obj)
    
    srt_list = []
    with open(parsed) as f:
        lines = [x.strip() for x in f.readlines()]
    i = 0
    for line in lines:
        if line.startswith("["):
            i += 1
            srt_obj = f"{i}. {[x for x in list(set(eval(line))) if x != '']}"
            srt_list.append(srt_obj)
    srt_process(subs, fallback_list, srt_list)

def batch_process(fallback_list, srt_list):
    # Split and process srt list into batches
    conv = None
    batch_count = math.ceil(len("\n".join(srt_list)) / 2000)+1
    print(batch_count, len("\n".join(srt_list)) / 2000)
    skip = len(srt_list)//batch_count
    batch = [srt_list[i:i+skip] for i in range(0,len(srt_list),skip)]
    outs = []
    for i in range(len(batch)):
        b = batch[i]
        prompt = PROMPT.replace("FALLBACK_LANGUAGE", FALLBACK_LANGUAGE)
        prompt = prompt.replace("LANGUAGE", LANGUAGE)
        prompt = prompt.replace("PARSED_TEXT", "\n".join(b))
        fallback = []
        for j in range(len(b)):
            id = int(b[j].split()[0].strip()[:-1])-1
            fallback.append(fallback_list[id])
        prompt = prompt.replace("FALLBACK_TEXT", "\n".join(fallback))
        print(prompt)
        out, conv = edgegpt(prompt, COOKIE_VALUE, conv)
        outs.append(out)
        time.sleep(5)
    return outs

def srt_process(subs, fallback_list, srt_list):
    print("[*] Processing SRT...")
    # Parse batches into one and update subs with translated text
    outs = batch_process(fallback_list, srt_list)
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
        
        # TODO: Translate text using google translate on last run if the past runs fails
        if j == runs-1:
            """
            for i in range(len(retries)):
                num, text =  int(retries[i].split()[0][:-1]), retries[i].split()[1:]
                text = " ".join(text).strip()
                translated = GoogleTranslator(source=FROM_LANG, target=LANG).translate(text=text)
                subs[num-1].text = translated
                changes[num-1] = True
            """
            break

        # Parse batches into one and update subs with translated text
        outs = batch_process(fallback_list, retries)
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
    with open('../output/processed.srt', 'w') as f:
        f.write(subs_output)
    print(subs_output)
                      

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 ai_compare_translate.py fallback.srt parsed.srt")
    else:
        print("[*] Parsing...")
        srt_parse(sys.argv[1], sys.argv[2])


