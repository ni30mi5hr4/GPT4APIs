import requests
import json

# Base URL and session hash
BASE_URL = "https://micka18-tiger.hf.space"
SESSION_HASH = "ci181aewtu"

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/?__theme=system",
}

# Stores chat history
chat_history = []

def send_request(endpoint, data):
    """Sends a POST request to the API and returns the JSON response."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("\nError sending request:", str(e))
        return {}

def stream_data(session_hash):
    """Streams real-time responses from the API queue."""
    url = f"{BASE_URL}/gradio_api/queue/data?session_hash={session_hash}"
    response = requests.get(url, headers=HEADERS, stream=True)

    print("\nStreaming response:\n", end="", flush=True)
    final_response = ""  # Store full response

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").strip()
            if decoded_line.startswith("data:"):
                try:
                    data = json.loads(decoded_line[len("data:"):].strip())

                    if data.get("msg") == "process_generating":
                        output_data = data["output"].get("data", [])
                        if output_data and isinstance(output_data[0], list) and len(output_data[0]) > 0:
                            text_chunk = output_data[0][-1][-1]  # Latest response chunk
                            print(text_chunk, end=" ", flush=True)
                            final_response += text_chunk + " "

                    elif data.get("msg") == "process_completed":
                        print("\n\nFinal Response:", final_response.strip())  # Print final response
                        return final_response.strip()  # Return response

                except (json.JSONDecodeError, IndexError, KeyError) as e:
                    print("\nError processing response:", str(e))
    return ""

def main():
    """Main function to send requests and maintain conversation."""
    global chat_history  # Access global chat history
    
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("\nYou: ")  # Ask for user input
        if user_input.lower() == "exit":
            print("Exiting chat...")
            break

        # Append new user message to chat history
        chat_history.append([user_input, None])  

        # Step 1: Send initial request
        request_data = {
            "data": [user_input, chat_history],  # Pass chat history
            "event_data": None,
            "fn_index": 0,
            "trigger_id": 8,
            "session_hash": SESSION_HASH,
        }

        response = send_request("/gradio_api/run/predict?__theme=system", request_data)

        # Step 2: Join the queue
        queue_data = {
            "data": [None, chat_history, "You are a friendly Chatbot.", 512, 0.7, 0.95],
            "event_data": None,
            "fn_index": 2,
            "trigger_id": 8,
            "session_hash": SESSION_HASH,
        }

        queue_response = send_request("/gradio_api/queue/join?__theme=system", queue_data)

        # Step 3: Stream response
        bot_response = stream_data(SESSION_HASH)

        # Append bot response to chat history
        if bot_response:
            chat_history[-1][1] = bot_response  # Store bot response

if __name__ == "__main__":
    main()
