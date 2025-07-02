#!/bin/bash

url='https://www.blackbox.ai/api/chat'
headers='Cookie: sessionId=dc6b94e8-4cb3-44d0-a00f-345c1083e374; personalId=dc6b94e8-4cb3-44d0-a00f-345c1083e374; g_state={"i_p":1710667247859,"i_l":1}; intercom-id-jlmqxicb=f284bc17-3c0a-4712-8947-eca99bb21b93; intercom-session-jlmqxicb=; intercom-device-id-jlmqxicb=45db7d96-3a0b-486d-8fcd-10ce8f887836'
headers+='User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
headers+='Accept: */*'
headers+='Accept-Language: en-US,en;q=0.5'
headers+='Accept-Encoding: gzip, deflate, br'
headers+='Referer: https://www.blackbox.ai/chat/expert-youtube'
headers+='Content-Type: application/json'
headers+='Origin: https://www.blackbox.ai'
headers+='Sec-Fetch-Dest: empty'
headers+='Sec-Fetch-Mode: cors'
headers+='Sec-Fetch-Site: same-origin'
headers+='Te: trailers'

data='{
  "messages": [{"id": "l8cZpS0", "content": "hey", "role": "user"}],
  "previewToken": null,
  "userId": "a9595e73-d057-49ed-9c32-8fac0efa32b2",
  "codeModelMode": true,
  "agentMode": {},
  "trendingAgentMode": {"mode": true, "id": "youtube"},
  "isMicMode": false,
  "isChromeExt": false,
  "githubToken": null
}'

curl -X POST -H "$headers" -d "$data" "$url"
