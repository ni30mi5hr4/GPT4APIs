"""A reverse engineering of GPT-4 from https://gpt4free.io."""

import random
import string
import json
import html
import re

import requests


LETTERS = string.ascii_lowercase + string.digits


def gpt4(prompt: str, system: str = None) -> str:
    """Fetches a response with GPT-4."""
    nonce = json.loads(
        html.unescape(
            re.findall(
                r"data-system=\"(.*?)\"",
                requests.get("https://gpt4free.io/chat", timeout=10).text,
            )[0]
        )
    )["restNonce"]
    gpt_response = []

    req = requests.post(
        "https://gpt4free.io/wp-json/mwai-ui/v1/chats/submit",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "text/event-stream",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "X-WP-Nonce": nonce,
            "Sec-GPC": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "referrer": "https://gpt4free.io/chat/",
        },
        json={
            "botId": "default",
            "customId": None,
            "session": "N/A",
            "chatId": "".join(random.choice(LETTERS) for _ in range(10)),
            "contextId": random.randint(0, 9999),
            "messages": [
                {
                    "content": system or "You are a helpful assistant.",
                    "id": "".join(random.choice(LETTERS) for _ in range(10)),
                    "role": "system",
                }
            ],
            "newMessage": prompt,
            "newFileId": None,
            "stream": True,
        },
        timeout=10,
    ).text

    json_tokens = [token.strip() for token in req.split("data:")][:-1][1:]
    for token in json_tokens:
        doc = json.loads(token)
        content = doc["data"]
        gpt_response.append(content)

    return "".join(gpt_response)


print("Enter a system prompt or press ENTER to use a default one.")
system_prompt = input("> ") or None

print("How can I help you today?")
while True:
    message = input("> ")
    print(gpt4(message, system_prompt))
