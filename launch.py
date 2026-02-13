import os
import subprocess

def update_env(client_name, data_path, system_prompt):
    env_content = f"""CLIENT_NAME="{client_name}"
DATA_PATH="{data_path}"
SYSTEM_PROMPT="{system_prompt}"
"""
    with open(".env", "w") as f:
        f.write(env_content)
    print(f"--- Environment updated for: {client_name} ---")

def main():
    print("Select an AI Agent Persona to launch:")
    print("1. Jose Rizal (Historical Digital Twin)")
    print("2. Modern Real Estate (Business Consultant)")
    
    choice = input("\nEnter choice (1 or 2): ")

    if choice == "1":
        update_env(
            "Jose Rizal", 
            "data/persona_context.txt", 
            "You are a digital twin of Dr. Jose Rizal. Maintain an intellectual, gentlemanly tone."
        )
    elif choice == "2":
        update_env(
            "Modern Real Estate", 
            "data/real_estate_faqs.txt", 
            "You are a professional real estate consultant. Be helpful and direct."
        )
    else:
        print("Invalid choice.")
        return

    # Launch the FastAPI server using uvicorn
    print("Starting server...")
    subprocess.run(["uvicorn", "app.main:app", "--reload"])

if __name__ == "__main__":
    main()