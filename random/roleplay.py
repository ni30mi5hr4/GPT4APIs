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

def send_request(endpoint, data):
    """Sends a POST request to the API and prints the raw JSON response."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        raw_response = response.json()  # Get raw JSON
        print("\n🔹 RAW API RESPONSE:\n", json.dumps(raw_response, indent=4))  # Pretty print
        return raw_response
    except requests.exceptions.RequestException as e:
        print("\n❌ Error sending request:", str(e))
        return {}

def extract_clean_response(data):
    """Extracts the clean response from the [[[ ]]] format."""
    try:
        if "output" in data and "data" in data["output"]:
            output_data = data["output"]["data"]
            if isinstance(output_data, list) and output_data:
                extracted_text = output_data[0][-1][-1]  # Extract final response text
                return extracted_text.strip() if extracted_text else "❌ No valid response."
    except (IndexError, KeyError, TypeError):
        return "❌ Error extracting response."
    return "❌ No response found."

def stream_data(session_hash):
    """Streams raw responses from the API queue and extracts the final output."""
    url = f"{BASE_URL}/gradio_api/queue/data?session_hash={session_hash}"
    response = requests.get(url, headers=HEADERS, stream=True)

    print("\n🔹 STREAMING RAW RESPONSE:\n", end="", flush=True)
    final_output = ""

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8").strip()
            print(decoded_line)  # Print raw line for debugging

            if decoded_line.startswith("data:"):
                try:
                    data = json.loads(decoded_line[len("data:"):].strip())

                    # Process final output
                    if data.get("msg") == "process_completed":
                        final_output = extract_clean_response(data)
                        break  # Stop after final response

                except (json.JSONDecodeError, IndexError, KeyError) as e:
                    print("\n❌ Error processing response:", str(e))

    print("\n\n🔹 FINAL CLEAN RESPONSE:\n", final_output)
    return final_output

def main():
    """Main function to send requests and print clean extracted responses."""
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Exiting chat...")
            break

        # Send initial request
        request_data = {
            "data": [user_input, []],  # No chat history for raw response
            "event_data": None,
            "fn_index": 0,
            "trigger_id": 8,
            "session_hash": SESSION_HASH,
        }

        send_request("/gradio_api/run/predict?__theme=system", request_data)

        # Join the queue
        queue_data = {
            "data": [None, [], "You are a friendly Chatbot.", 512, 0.7, 0.95],
            "event_data": None,
            "fn_index": 2,
            "trigger_id": 8,
            "session_hash": SESSION_HASH,
        }

        send_request("/gradio_api/queue/join?__theme=system", queue_data)

        # Stream raw response with clean extracted output
        stream_data(SESSION_HASH)

if __name__ == "__main__":
    main()
