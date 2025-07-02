import requests
import json
import cowsay
import os

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

    response = requests.post(url, json=payload, headers=headers, stream=True)
    full_text = ''
    for line in response.iter_lines():
        decoded_line = line.decode('utf-8').strip()
        if decoded_line.startswith('data: '):
            json_str = decoded_line[len('data: '):]
            try:
                data = json.loads(json_str)
                content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                full_text += content
            except json.JSONDecodeError:
                pass

    return full_text

def clear_screen():
    # Clear the console screen. This works on Windows and Unix-based systems (Linux, macOS).
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        print("\nWhat would you like to do?")
        print("1: Ask a question")
        print("2: Clear screen")
        print("3: Exit")

        user_choice = input("Enter your choice (1, 2, or 3) or ask your question directly: ")

        if user_choice == '1' or user_choice not in ['2', '3']:
            if user_choice == '1':
                user_question = input("Please enter your question: ")
            else:
                user_question = user_choice
            response_text = get_response_from_api(user_question)
            cowsay.tux("Response: " + response_text)
        elif user_choice == '2':
            clear_screen()
        elif user_choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
