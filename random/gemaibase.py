import requests
import json
import time
import os
import sys
import threading

def send_query(query):
    url = "https://nixchamp-geminipro.hf.space/"
    payload = {"q": query}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def show_progress_bar():
    sys.stdout.write("Processing: [")
    sys.stdout.flush()
    for _ in range(50):
        time.sleep(0.05)  # Adjust sleep time for a better visual effect
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("] Done\n")

def process_request(query):
    print("Processing your request...")
    thread = threading.Thread(target=show_progress_bar)
    thread.start()
    result = send_query(query)
    thread.join()

    return result

def main():
    chatting_mode = True  # Assume we're always in "chatting mode" for the purpose of this code

    while True:
        print("\nMenu Options:")
        print("1. Ask a question")
        print("2. Clear screen")
        print("3. Exit")
        option = input("Choose an option (1/2/3) or enter your question directly: ")

        if option.strip() == "1":
            query = input("Enter your question: ")
            if query.lower() == "exit":
                break
            start_time = time.time()
            result = process_request(query)
            if result is not None and 'message' in result:
                message = result['message']
                print("\n" + "-" * 50)
                print(f"{message}\n")
                print("-" * 50)
            else:
                print("No message found in the response.")
            end_time = time.time()
            print(f"Processing time: {end_time - start_time} seconds")

        elif option.strip() == "2":
            clear_screen()

        elif option.strip() == "3" or option.lower().strip() == "exit":
            break

        elif option.strip():
            start_time = time.time()
            result = process_request(option)
            if result is not None and 'message' in result:
                message = result['message']
                print("\n" + "-" * 50)
                print(f"{message}\n")
                print("-" * 50)
            else:
                print("No message found in the response.")
            end_time = time.time()
            print(f"Processing time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
