import requests

url = 'https://www.blackbox.ai/api/chat'
headers = {
    'Cookie': 'sessionId=dc6b94e8-4cb3-44d0-a00f-345c1083e374; personalId=dc6b94e8-4cb3-44d0-a00f-345c1083e374; g_state={"i_p":1710667247859,"i_l":1}; intercom-id-jlmqxicb=f284bc17-3c0a-4712-8947-eca99bb21b93; intercom-session-jlmqxicb=; intercom-device-id-jlmqxicb=45db7d96-3a0b-486d-8fcd-10ce8f887836',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.blackbox.ai/chat/expert-youtube',
    'Content-Type': 'application/json',
    'Origin': 'https://www.blackbox.ai',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Te': 'trailers'
}
data = {
    "messages": [{"id": "l8cZpS0", "content": "hey", "role": "user"}],
    "previewToken": None,
    "userId": "a9595e73-d057-49ed-9c32-8fac0efa32b2",
    "codeModelMode": True,
    "agentMode": {},
    "trendingAgentMode": {"mode": True, "id": "youtube"},
    "isMicMode": False,
    "isChromeExt": False,
    "githubToken": None
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.text)
