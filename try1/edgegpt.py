import json
import requests as req
from urllib.parse import quote
from websocket import WebSocket
import re
import os
import sys


def edgegpt(prompt_message):
  cookie_value = "_EDGE_V=1; USRLOC=HS=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=6D0C3E4299CB4DA0BCF316DB733040DE&dmnchg=1; MSCC=cid=s0k1fscuqm1w4tf00ismxwdz-c1=1-c2=1-c3=1; MUID=34CFC4BDFCC868530083D7CEFD3D6953; MUIDB=34CFC4BDFCC868530083D7CEFD3D6953; BCP=AD=0&AL=0&SM=0&CS=M; MMCASM=ID=874EAB27530D476197E693B9E981A456; _UR=; ANON=A=EAEE091FDB6789E32CF85341FFFFFFFF&E=1cec&W=1; NAP=V=1.9&E=1c92&C=fHR1gmbm0js1ue32lLSeTTgQIW9DUVLDr753eOMuEx0lJOkP6IFqXQ&W=1; PPLState=1; KievRPSSecAuth=FABSBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACLBTXE78TsY+EAR6NJPVOCslcn6FTUwE7+uWRuc4ROt1BOFNn1TQtAJBK3c1sP0MVqj+Q7ogXOQ7OLRyHdiz2Dt0H0DQ6JSErPIXnSjurwaq+nOZ0phKaXIMhzU+nkn44R4toWXiq4psQxqkJtkrr7i6FBLJdLRITvLPt+T387SYcS4ojFn8kNeterJPQReCun4Z8EtA4i3KJz3NdwhK0yVfj+vpP3TGwGHODnASzLhO0oAD6YfdX6YSc9aAKtfKy5BHOJGkSm/0TxxiXTotPp8sbNFda6y4TjEcSr6fRNUDYU9F5ApZhU6Ih3OEsdOW/AkCzxT+SlIqHUp23fDuPdq9FfRh0A3oYJPNb8YP3GeYFt6pZVMpy79wkwgiypozz9MoqBSvrf89Ea6QQhCF8N4eRedqk1oAN31OkK+vAFwOhu/hP7X/LsZspzPMKYZyn9WW20/oRDvVIIb8oRkfhOusPkGTSFXHkBYQqVZJ6w3M21FjAfvLd7tuIHDuqdNNXsTFd2D0syWdYfnn01MV3fzr8hW6svFbAHmAC56+ggPJoKLbDOgnQuQ0vSbPlObHsUghww1MG+0dhqwuPrU5/oZbVG58qcyNRpuclrrjcyoAuVIdlsAIoqg/tZsQJE2Pxcep7s3sTtzSQzU8rdjTi2wn/EgS3HnYT6ItpfELwox1bWM9qlXwWzjQZvoS/QdNY91GB3plbm/CUDdle5Si5VT17V1Ac7NTl64HUpRi3bBlJ9Pv+5JLuYx2csMz8N/qSjEmEvn8jwqiLqmSnhR7pIOkwrXo1VmJFlKyId1N8yR4Pi20Vh/vsIgOp2rryxlo0FudbZflWaiIzIM+fw//xxpnF5BcmPvp1+u5BBR//PLew6Kpin3Xosxz/y08I5uyzerOZ+diwM35TQ+OF1XREYRLRC9pEW0TL1lczz/49TY6NedjSjJ0rn/Qbh02oK+aWN29xvEUWTS9kwjw4Ho3Xr8LpHJN9kjaN4U5fpVHRGas5oPRJ0XtGmRvN3cv+51JeqtT29ipBzDJB08bi/7QvZKaI9F/WfW/M+Bryhtec+W2ofnreoqhPaBYpNRhVwkGRIr+d7/Q8fF/7iDzcry7aa4yzOwjRxGadrmv2jxZySSlXyNpSFu2eGfJ3pVi+vr5T7POrnB9VxDi4WuMMfTaBajNznExZW2NGiLU3v/EXT1D1tGLul2gVShlhGldilB7zde7p94tzkssi5kqR0kskQfXBcoxrcxEdRkWYxRLeke2EZf0Jh8GrInFB6jVCO/NQsBx44TigTbcmTafDtvVPPpanmOQcajDywOPovWH0ILeghrypnIB2RRpeFAzvQKG0wqBUZwCIJU959PzS+0XDXGDIEL59vgM7/wY3dKbtQsNl0ARmYq8elB2jRQARG+isjCKN/YJbIcGLnj3q042tjs=; fdfre=o=1; _ITAB=STAB=FD; _clck=npi7v8|2|fgr|0|1392; EDGSRCHHPGUSR=udstone=Creative&udstoneopts=h3imaginative,gencontentv3,fluxv1,flxegctxv2,egctxcplt,egcpltsum&CIBV=1.1381.12; _EDGE_S=SID=2C5A202474AD677717A733D375FA6613; WLS=C=ebf6b835dc47dc10&N=Jonny; _Rwho=u=d; _SS=SID=2C5A202474AD677717A733D375FA6613&R=1205&RB=1205&GB=0&RG=3780&RP=1205&PC=HCTS; SRCHS=PC=HCTS; SRCHUSR=DOB=20230820&T=1703970715000; MSPTC=w35K5pyoCTPqQMqeotjLzo1K8kukPsBTVhMvvL_xkSU; ipv6=hit=1703974324224&t=4; dsc=order=News; _RwBf=r=0&ilt=0&ihpd=0&ispd=0&rc=1205&rb=1205&gb=0&rg=3780&pc=1205&mtu=0&rbb=0&g=0&cid=&clo=0&v=8&l=2023-12-30T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=bingcopilotwaitlist&c=MY00IA&t=6412&s=2023-02-20T11:16:38.4844145+00:00&ts=2023-12-30T21:30:25.2193923+00:00&rwred=0&wls=2&wlb=0&lka=0&lkt=0&TH=&mta=0&e=fYmSVTdEoN3iis4dTgXkejp4IbTFzs6_myYGBhCcg3qiCO6f2JwWOPuG8ihFKs4mQlrpZIjXXZSjgP9X1wpL7Xs50rW1TkEXDOwkMa3X0iQ&A=EAEE091FDB6789E32CF85341FFFFFFFF&aad=0&ard=0001-01-01T00:00:00.0000000&wle=0&ccp=0; _U=1v_uM8FHE1c-ih7cmcddQnLaBJ5Lh0S8IMb-6GANNhwR5ibepd_KjxdK0QXqgT9LegfzQukT7oUgZnFMQXttxikI4PRAH1pI1kY2FazihYdhQrAQsjG37gQopFRDLFrmL6BHKXZ6DCGwXKZY-M8es4MKcruRUmh9n2gU_yuGWIoh4HYQmykqSpLJwkBJ3UY1pTTxCiml9ibbgD0G44S8v3w; GC=Q52W33L-JbGOqlfyRr8Al4cSwShwYaPvu_tpFlkq8KzKTyfqfF6IPaRU1PORiq0yc7V3VFQJAnfZtV1NQiOEGA; SRCHHPGUSR=SRCHLANG=en&PV=15.0.0&BRW=NOTP&BRH=M&CW=840&CH=928&SCW=840&SCH=796&DPR=1.0&UTC=60&DM=1&EXLTT=31&HV=1703971829&PRVCW=1860&PRVCH=928&CIBV=1.1381.12&cdxtone=Precise&cdxtoneopts=h3precise,clgalileo,gencontentv3" # Update cookie_value here
  cookie_split = [x.strip().replace("=","ÅÅÅ",1).split("ÅÅÅ") for x in cookie_value.split(';')]

  sess = req.Session()
  cookies = {}
  for cookie in cookie_split:
      cookies[cookie[0]] = cookie[1]
      sess.cookies.set(cookie[0], cookie[1], domain=".bing.com")
  cookies = "; ".join([f"{x[0]}={x[1]}" for x in sess.cookies.items()])

  res = sess.get("https://www.bing.com/turing/conversation/create?bundleVersion=1.1381.12")
  conversation = res.json()
  appid = "6c0f12ef-97d3-4869-bc42-c1d9bdb4a759"
  plugin_id = "c310c353-b9f0-4d76-ab0d-1dd5e979cf68"
  client_id = conversation["clientId"]
  conversation_id = conversation["conversationId"]
  conversation_signature = res.headers["X-Sydney-Conversationsignature"]
  encrypted_conversation_signature = res.headers["X-Sydney-Encryptedconversationsignature"]

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
        "isStartOfSession": True,
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
    "invocationId": "0",
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
              invalid_runs = 0
              if "END" in text:
                  pattern = re.compile(r"START(.*?)END", re.DOTALL)
                  out = pattern.findall(text)[0].strip()
                  run = False
                  break
      except Exception as e:
          pass
  print()
  return out

if __name__ == "__main__":
  prompt_message = """
  Here is a list of parsed vietnamese subtitle texts:
  ['. mm me\n\nHơậ hỗn những diều dó.', 'Hơi hẳn những diều dó.', 'Hơệ hẳn những diều đó.', 'Hơệ hẳn những diều đó.', 'Hơộ hẳn những diều đó.', 'Hơô hẳn những diều dó.', 'Hơn hẳn những diều dó.', 'Hơn liễn những diều dó.', 'Hơn lển những diều dó.', 'Hơn HỂn những diều dó.', 'Hơn tê những điều đỏ.', 'Hơn hệ những điều đỏ.']
  
  Can you help me clean it up and from all the outputs guess what the correct message is? If you believe something is an abbrevation or doesn't fit in the message please do not include it. Write your answer in the following format, take for example if the answer is "ANSWER":
  
  START
  ANSWER
  END
  """
  print(edgegpt(prompt_message))



