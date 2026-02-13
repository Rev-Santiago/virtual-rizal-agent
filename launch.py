import os
import subprocess

def update_env(client_name, data_path, system_prompt):
    """Overwrites the .env file with new client details."""
    env_content = f"""CLIENT_NAME="{client_name}"
DATA_PATH="{data_path}"
SYSTEM_PROMPT="{system_prompt}"
"""
    with open(".env", "w") as f:
        f.write(env_content)
    print(f"\n[SYSTEM] Configuration switched to: {client_name}")

def main():
    print("--- White-Label Configuration Switcher ---")
    print("1. Jose Rizal (Historical Digital Twin)")
    print("2. Modern Real Estate (Business Consultant)")
    
    choice = input("\nSelect a persona (1 or 2): ")

    if choice == "1":
        update_env(
            "Jose Rizal", 
            "data/persona_context.txt", 
            "You are a digital twin of Dr. Jose Rizal. Maintain an intellectual, gentlemanly tone. Address the user as Ginoo or Binibini."
        )
    elif choice == "2":
        update_env(
            "Modern Real Estate", 
            "data/real_estate_faqs.txt", 
            "You are a professional real estate consultant for Modern Metro. "
            "Your knowledge is strictly limited to the provided Context. "
            "RULES: "
            "1. Answer ONLY using facts explicitly written in the Context. "
            "2. If the Context says we have 'listings' but doesn't name them, do NOT invent specific property names or details. "
            "3. Do NOT use placeholders like '[Property 1]' or make up amenities. "
            "4. If you lack specific details, offer to book a viewing instead."
        )
    else:
        print("Invalid choice.")
        return

    # Commented out for Docker usage:
    # print("Starting server...")
    # subprocess.run(["uvicorn", "app.main:app", "--reload"])

    print("\n[NEXT STEP] Run 'docker-compose up --build' (or restart the container) to apply changes.")

if __name__ == "__main__":
    main()