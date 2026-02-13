import requests
import config  # Pulls the current CLIENT_NAME from .env

def clear_memory():
    """Sends a request to the server to wipe the conversation history."""
    url = "http://127.0.0.1:8000/clear_history"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(f"\n[SYSTEM] Conversation history cleared for {config.CLIENT_NAME}.\n")
        else:
            print(f"\n[ERROR] Could not clear history: {response.text}\n")
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}\n")

def chat_with_agent(message):
    url = "http://127.0.0.1:8000/chat"
    payload = {"message": message}
    
    try:
        # stream=True handles the word-by-word response
        with requests.post(url, json=payload, stream=True, timeout=60) as response:
            if response.status_code == 200:
                print(f"{config.CLIENT_NAME}: ", end="", flush=True)
                
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        print(chunk, end="", flush=True)
                print() 
            else:
                print(f"Server Error ({response.status_code}): {response.text}")

    except requests.exceptions.Timeout:
        print("\nError: The request timed out.")
    except Exception as e:
        print(f"\nConnection Error: {e}")

if __name__ == "__main__":
    print(f"--- {config.CLIENT_NAME} Test Client ---")
    print("Type 'quit' to exit.")
    print("Type '/clear' to reset conversation memory.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit']:
            break
        
        # Check for the special clear command
        if user_input.lower() == '/clear':
            clear_memory()
            continue
            
        chat_with_agent(user_input)