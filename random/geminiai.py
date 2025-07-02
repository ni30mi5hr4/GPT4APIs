import requests
import json

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

def main():
    while True:
        query = input("Enter your question (or type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        result = send_query(query)
        if result is not None and 'message' in result:
            message = result['message']
            print("\n" + "-" * 50)
            print(f"{message}\n")
            print("-" * 50)
        else:
            print("No message found in the response.")

if __name__ == "__main__":
    main()
