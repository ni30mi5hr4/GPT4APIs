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
        print("\n❌ Error sending request:", str(e))
        return {}


def extract_clean_response(data):
    """Extracts the clean response from the [[[ ]]] format."""
    try:
        if "output" in data and "data" in data["output"]:
            output_data = data["output"]["data"]
            if isinstance(output_data, list) and output_data:
                return output_data[0][-1][-1].strip() if output_data[0][-1] else "❌ No valid response."
    except (IndexError, KeyError, TypeError):
        return "❌ Error extracting response."
    return "❌ No response found."


def stream_data(session_hash):
    """Streams raw responses from the API queue and extracts the final output."""
    url = f"{BASE_URL}/gradio_api/queue/data?session_hash={session_hash}"
    response = requests.get(url, headers=HEADERS, stream=True)

    final_output = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").strip()

            if decoded_line.startswith("data:"):
                try:
                    data = json.loads(decoded_line[len("data:"):].strip())

                    if data.get("msg") == "process_completed":
                        final_output = extract_clean_response(data)
                        break  # Stop after final response

                except (json.JSONDecodeError, IndexError, KeyError) as e:
                    print("\n❌ Error processing response:", str(e))

    return final_output


def main():
    """Main function to send requests and maintain conversation history."""
    global chat_history  # Access global chat history

    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Exiting chat...")
            break

        # Append new user message to chat history
        chat_history.append([user_input, None])

        # Send initial request with chat history
        request_data = {
            "data": [user_input, chat_history],  # Pass chat history
            "event_data": None,
            "fn_index": 0,
            "trigger_id": 8,
            "session_hash": SESSION_HASH,
        }

        send_request("/gradio_api/run/predict?__theme=system", request_data)

        # Join the queue with chat history
        queue_data = {
            "data": [None, chat_history, "You are a friendly Chatbot.", 1536, 0.7, 0.95],
            "event_data": None,
            "fn_index": 2,
            "trigger_id": 8,
            "session_hash": SESSION_HASH,
        }

        send_request("/gradio_api/queue/join?__theme=system", queue_data)

        # Stream response and update chat history
        bot_response = stream_data(SESSION_HASH)

        if bot_response:
            chat_history[-1][1] = bot_response  # Store bot response
            print(f"\nBot: {bot_response}")  # Show bot's response


if __name__ == "__main__":
    main()
