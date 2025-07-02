import requests
import json

def get_response_from_api(question):
    url = "https://api.gptcall.net/v1/chat/completions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://gptcall.net/",
        "Content-Type": "application/json",
        "Authorization": "hifredi",
        "Origin": "https://gptcall.net",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Te": "trailers"
    }

    payload = {
        "messages": [{"role": "user", "content": question}],
        "stream": True,
        "model": "gpt-3.5-turbo",
        "additional": {"authToken": "", "openrouter": ""}
    }

    # Sending request
    response = requests.post(url, json=payload, headers=headers, stream=True)

    # Initialize an empty string to hold the concatenated text
    full_text = ''

    # Process the streamed response
    for line in response.iter_lines():
        # Decode line to text (from bytes) and strip whitespace
        decoded_line = line.decode('utf-8').strip()
        if decoded_line.startswith('data: '):  # Check for the 'data: ' prefix
            json_str = decoded_line[len('data: '):]
            try:
                # Parse the JSON string into a Python dictionary
                data = json.loads(json_str)

                # Extract the 'content' field from the response and append it to our full_text string
                content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                full_text += content
            except json.JSONDecodeError:
                # Skip failed JSON parsing without printing any warning
                pass

    return full_text

# Prompt the user to input their question
user_question = input("Please enter your question: ")

# Get the response from the API
response_text = get_response_from_api(user_question)

# Print the response text
print("Response:", response_text)
