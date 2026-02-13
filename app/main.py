from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage
from app.engine import create_white_label_agent
import config

app = FastAPI(title=f"{config.CLIENT_NAME} AI Agent")

# Initialize the agent
agent = create_white_label_agent(config.DATA_PATH, config.SYSTEM_PROMPT)

# Simple in-memory history (clears when server restarts)
CHAT_HISTORY = []

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {config.CLIENT_NAME} API"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # 1. Prepare the input with history
    chain_input = {
        "question": request.message,
        "chat_history": CHAT_HISTORY
    }

    # 2. Stream the response and build the full answer for history
    async def stream_response():
        full_response = ""
        async for chunk in agent.astream(chain_input):
            full_response += chunk
            yield chunk
        
        # 3. Update History after full generation
        CHAT_HISTORY.append(HumanMessage(content=request.message))
        CHAT_HISTORY.append(AIMessage(content=full_response))

    return StreamingResponse(stream_response(), media_type="text/plain")

@app.post("/clear_history")
async def clear_history():
    global CHAT_HISTORY
    CHAT_HISTORY = []
    return {"status": "History cleared"}