import json
import requests as req
from urllib.parse import quote
from websocket import WebSocket
import re
import os
import sys

def edgegpt(prompt_message, cookie_value, conv=None):
    cookie_split = [x.strip().replace("=","ÅÅÅ",1).split("ÅÅÅ") for x in cookie_value.split(';')]
    
    sess = req.Session()
    cookies = {}
    for cookie in cookie_split:
        cookies[cookie[0]] = cookie[1]
        sess.cookies.set(cookie[0], cookie[1], domain=".bing.com")
    cookies = "; ".join([f"{x[0]}={x[1]}" for x in sess.cookies.items()])

    # Create new conversation if not initialized or conversation exceed max messages
    appid = "6c0f12ef-97d3-4869-bc42-c1d9bdb4a759"
    plugin_id = "c310c353-b9f0-4d76-ab0d-1dd5e979cf68"
    if not conv or conv.get('messages', 0) > 28:
        res = sess.get("https://www.bing.com/turing/conversation/create?bundleVersion=1.1381.12")
        conversation = res.json()
        client_id = conversation["clientId"]
        conversation_id = conversation["conversationId"]
        conversation_signature = res.headers["X-Sydney-Conversationsignature"]
        encrypted_conversation_signature = res.headers["X-Sydney-Encryptedconversationsignature"]

        conv = {"messages": 1, "conversation_id": conversation_id}
    else:
        conversation_id = conv["conversation_id"]
        res = sess.get(f"https://www.bing.com/turing/conversation/create?conversationId={quote(conversation_id)}&bundleVersion=1.1381.12")
        conversation = res.json()
        client_id = conversation["clientId"]
        conversation_id = conversation["conversationId"]
        conversation_signature = res.headers["X-Sydney-Conversationsignature"]
        encrypted_conversation_signature = res.headers["X-Sydney-Encryptedconversationsignature"]

        conv["messages"] += 1

    add_conversation_url = f"https://www.bing.com/codex/plugins/conversation/add?conversationId={quote(conversation_id)}&appid={appid}&pluginId={plugin_id}"
    res = sess.post(add_conversation_url)
    res = res.json()

    if not res.get('IsSuccess', False):
        return ""

    chathub_url = f"wss://sydney.bing.com/sydney/ChatHub?sec_access_token={quote(encrypted_conversation_signature).replace('/','%2F')}"
    def as_json(message):
        DELIMETER = "\x1e"  # Record separator character.
        return json.dumps(message) + DELIMETER

    cookies = "; ".join([f"{x[0]}={x[1]}" for x in sess.cookies.items()])

    ws = WebSocket()
    ws.connect(chathub_url, cookie=cookies)
    ws.send(as_json({"protocol": "json", "version": 1}))
    ws.recv()
    ws.send(as_json({"type":6}))
    ws.send(as_json({
    "arguments": [
      {
        "source": "cib",
        "optionsSets": [
          "nlu_direct_response_filter",
          "deepleo",
          "disable_emoji_spoken_text",
          "responsible_ai_policy_235",
          "enablemm",
          "dv3sugg",
          "autosave",
          "iyxapbing",
          "iycapbing",
          "h3precise",
          "clgalileo",
          "gencontentv3",
          "eredirecturl"
        ],
        "allowedMessageTypes": [
          "ActionRequest",
          "Chat",
          "ConfirmationCard",
          "Context",
          "InternalSearchQuery",
          "InternalSearchResult",
          "Disengaged",
          "InternalLoaderMessage",
          "InvokeAction",
          "Progress",
          "RenderCardRequest",
          "RenderContentRequest",
          "AdsQuery",
          "SemanticSerp",
          "GenerateContentQuery",
          "SearchQuery"
        ],
        "sliceIds": [],
        "verbosity": "verbose",
        "scenario": "SERP",
        "plugins": [
          {
            "id": plugin_id
          }
        ],
        "conversationHistoryOptionsSets": [
          "autosave",
          "savemem",
          "uprofupd",
          "uprofgen"
        ],
        "isStartOfSession": conv["messages"] == 1,
        "message": {
          "locale": "en-US",
          "market": "en-US",
          "region": "NO",
          "author": "user",
          "inputMethod": "Keyboard",
          "text": prompt_message,
          "messageType": "Chat",
        },
        "tone": "Precise",
        "spokenTextMode": "None",
        "conversationId": conversation_id,
        "participant": {
          "id": client_id
        }
      }
    ],
    "invocationId": str(conv["messages"] - 1),
    "target": "chat",
    "type": 4
    }))

    out = ""
    run = True
    invalid_runs = 0
    while run and invalid_runs <= 10:
        print(".", end="", flush=True)
        invalid_runs += 1
        try:
            data = json.loads(ws.recv().strip())
            item = data.get("arguments", [])[0]
            messages = item.get("messages", [])
            for msg in messages:
                text = msg.get('text',"")
                # print(text, flush=True)
                invalid_runs = 0
                if "END" in text:
                    pattern = re.compile(r"START(.*?)END", re.DOTALL)
                    out = pattern.findall(text)[0].strip()
                    run = False
                    break
        except Exception as e:
            pass
    print()
    return out, conv

if __name__ == "__main__":
    cookie_value = open('.cookie').read()
    prompt_message = """
Here is a list of parsed vietnamese subtitle texts:
['', '', '', '', '', 'Sao thể ạ?', 'Sao thể ạ?', 'Sao thể ạ?', 'Sao thể ạ?', 'Sao thể ạ?', 'Sao thể ạ?', 'Sao thể ạ?']

Can you help me clean it up and from all the outputs guess what the correct message is? If you believe something is an abbrevation or doesn't fit in the message please do not include it. If you believe the parsed message came out bad and doesn't include anything meaninful, then write the answer as an empty space. Write your answer in the following format, take for example if the answer is "ANSWER":

START
ANSWER
END

Use the following english translation for this subtitle as a base of context for the sentence being corrected:
- Interesting.
-Is something the matter?

Do not write your thoughts, only give the answer.
"""
    out, conv = edgegpt(prompt_message, cookie_value)
    print(out, conv)
    out,conv = edgegpt("Can you repeat the answer again?", cookie_value, conv)
    print(out, conv)
    out,conv = edgegpt("Can you repeat the answer once again?", cookie_value, conv)
    print(out, conv)


