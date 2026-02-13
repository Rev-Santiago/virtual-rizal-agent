import os
from dotenv import load_dotenv

load_dotenv()

# Client-specific configurations
CLIENT_NAME = os.getenv("CLIENT_NAME", "General AI Agent")
# Updated to match your new filename
DATA_PATH = os.getenv("DATA_PATH", "data/persona_context.txt") 
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")

# The "System Persona" - defined in your .env for each client
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", (
    "You are a helpful and professional AI assistant. "
    "Use the provided context to answer questions accurately."
))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")