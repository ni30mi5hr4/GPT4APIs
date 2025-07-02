import requests

# Define the base URL and session hash
BASE_URL = "https://micka18-tiger.hf.space"
SESSION_HASH = "ci181aewtu"

# Define headers
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/?__theme=system",
}

def send_request(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

def stream_data(session_hash):
    url = f"{BASE_URL}/gradio_api/queue/data?session_hash={session_hash}"
    response = requests.get(url, headers=HEADERS, stream=True)

    for line in response.iter_lines():
        if line:
            # Decode the line as it comes in bytes
            decoded_line = line.decode('utf-8')
            # Skip any keep-alive new lines
            if decoded_line.strip() == '':
                continue
            # Print the data part of the SSE
            if decoded_line.startswith('data:'):
                data = decoded_line[len('data:'):].strip()
                print(data)

def main():
    # Example request data
    request_data = {
        "data": ["my name is Nick", []],
        "event_data": None,
        "fn_index": 0,
        "trigger_id": 8,
        "session_hash": SESSION_HASH
    }

    # Send initial request
    response = send_request("/gradio_api/run/predict?__theme=system", request_data)
    print("Initial Response:", response)

    # Join the queue
    queue_data = {
        "data": [None, [["Hi", None]], "You are a friendly Chatbot.", 512, 0.7, 0.95],
        "event_data": None,
        "fn_index": 2,
        "trigger_id": 8,
        "session_hash": SESSION_HASH
    }
    queue_response = send_request("/gradio_api/queue/join?__theme=system", queue_data)
    print("Queue Response:", queue_response)

    # Stream data from the queue
    print("Streaming data...")
    stream_data(SESSION_HASH)

if __name__ == "__main__":
    main()
