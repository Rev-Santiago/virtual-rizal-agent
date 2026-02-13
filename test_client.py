import requests
import json

def chat_with_agent(message):
    url = "http://127.0.0.1:8000/chat"
    payload = {"message": message}
    headers = {"Content-Type": "application/json"}

    try:
        # Added a longer timeout because local LLMs can be slow
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            try:
                print(f"Rizal: {response.json()['response']}")
            except json.decoder.JSONDecodeError:
                print("--- Debug: Received non-JSON response ---")
                print(f"Raw Content: {response.text}")
        else:
            print(f"Server Error ({response.status_code}): {response.text}")

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Your local AI is taking too long to respond.")
    except Exception as e:
        print(f"Connection Error: {e}")