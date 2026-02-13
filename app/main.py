from fastapi import FastAPI
from pydantic import BaseModel # Ensure this is imported
from app.engine import create_white_label_agent
import config

app = FastAPI(title=f"{config.CLIENT_NAME} AI Agent")

# Define the agent here so the routes can access it
# It uses the data path and persona defined in your config
agent = create_white_label_agent(config.DATA_PATH, config.SYSTEM_PROMPT)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def read_root():
    # Updated to use the dynamic client name from your config
    return {"message": f"Welcome to the {config.CLIENT_NAME} API"}

from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat(request: ChatRequest):
    # This uses the generator built into LangChain LCEL chains
    async def stream_response():
        async for chunk in agent.astream(request.message):
            yield chunk

    return StreamingResponse(stream_response(), media_type="text/plain")