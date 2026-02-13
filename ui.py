import streamlit as st
from audio_recorder_streamlit import audio_recorder
import requests
import config

# Page Config
st.set_page_config(page_title=f"{config.CLIENT_NAME} Interface", layout="centered")
st.title(f"🇵🇭 {config.CLIENT_NAME} Agent")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# --- VOICE INPUT ---
st.write("### 🎙️ Talk to the Agent")
# This creates a microphone button
audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=16000, text="", icon_size="2x")

if audio_bytes:
    # 1. Display User Audio Placeholder
    st.chat_message("user").markdown("🎤 *Voice Message Sent*")
    
    # 2. Send to Backend
    files = {"file": ("input.wav", audio_bytes, "audio/wav")}
    try:
        with st.spinner("Listening & Thinking..."):
            # Note: We use localhost because Docker maps port 8000 to your machine
            response = requests.post("http://localhost:8000/chat/voice", files=files)
        
        if response.status_code == 200:
            # Extract Text and Audio
            ai_text = response.headers.get("X-Text-Response", "Audio Response")
            
            # Display AI Response
            with st.chat_message("assistant"):
                st.markdown(ai_text)
                st.audio(response.content, format="audio/mp3")
            
            # Save to history so it stays when you refresh
            st.session_state.messages.append({"role": "user", "content": "🎤 *Voice Message*"})
            st.session_state.messages.append({"role": "assistant", "content": ai_text, "audio": response.content})
            
    except Exception as e:
        st.error(f"Connection Error: {e}")

# --- TEXT INPUT ---
if prompt := st.chat_input("Or type your message here..."):
    # Display User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send to Backend (Streaming)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with requests.post("http://localhost:8000/chat", json={"message": prompt}, stream=True) as r:
            for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})