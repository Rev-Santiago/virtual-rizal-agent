from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, FileResponse
from langchain_core.messages import HumanMessage, AIMessage
from app.engine import create_white_label_agent
from app.voice import transcribe_audio, text_to_speech # Import voice module
import config
import shutil
import os

app = FastAPI(title=f"{config.CLIENT_NAME} AI Agent")

# Initialize agent
agent = create_white_label_agent(config.DATA_PATH, config.SYSTEM_PROMPT)
CHAT_HISTORY = []

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {config.CLIENT_NAME} API"}

@app.post("/chat")
async def chat(request: ChatRequest):
    chain_input = {"question": request.message, "chat_history": CHAT_HISTORY}
    
    async def stream_response():
        full_response = ""
        async for chunk in agent.astream(chain_input):
            full_response += chunk
            yield chunk
        CHAT_HISTORY.append(HumanMessage(content=request.message))
        CHAT_HISTORY.append(AIMessage(content=full_response))

    return StreamingResponse(stream_response(), media_type="text/plain")

# --- NEW VOICE ENDPOINT ---
@app.post("/chat/voice")
async def chat_voice(file: UploadFile = File(...)):
    # 1. Save uploaded audio
    temp_input = "temp_input.wav"
    with open(temp_input, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Transcribe (STT)
    user_text = transcribe_audio(temp_input)
    print(f"User said: {user_text}")

    # 3. Generate AI Response (Text)
    chain_input = {"question": user_text, "chat_history": CHAT_HISTORY}
    ai_response_text = await agent.ainvoke(chain_input) # Non-streaming for audio
    
    # Update History
    CHAT_HISTORY.append(HumanMessage(content=user_text))
    CHAT_HISTORY.append(AIMessage(content=ai_response_text))

    # 4. Convert to Speech (TTS)
    output_audio = "temp_output.mp3"
    await text_to_speech(ai_response_text, output_audio)

    # 5. Return Audio File
    return FileResponse(output_audio, media_type="audio/mpeg", headers={"X-Text-Response": ai_response_text})

@app.post("/clear_history")
async def clear_history():
    global CHAT_HISTORY
    CHAT_HISTORY = []
    return {"status": "History cleared"}