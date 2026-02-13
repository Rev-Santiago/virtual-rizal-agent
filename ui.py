import streamlit as st
from audio_recorder_streamlit import audio_recorder
import requests
import config

st.set_page_config(page_title=f"{config.CLIENT_NAME} Interface", layout="centered")
st.title(f"🇵🇭 {config.CLIENT_NAME} Agent")

# 1. Initialize Session State for History and UI Persistence
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mic_key" not in st.session_state:
    st.session_state.mic_key = 0  # Used to force-reset the mic component

# 2. Sidebar for Mode Selection
with st.sidebar:
    st.header("Settings")
    # This toggle decides if the AI should respond with voice
    voice_mode = st.toggle("Enable Voice Response Mode", value=False)
    if st.button("Clear Chat History"):
        requests.post("http://localhost:8000/clear_history")
        st.session_state.messages = []
        st.rerun()

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# 4. Separate Input Logic
# We use a column layout to put the mic next to the header or at the bottom
st.divider()
st.write("### Interaction")

# --- VOICE INPUT (Only processes if audio is captured) ---
audio_bytes = audio_recorder(
    text="Click to speak", 
    icon_size="2x", 
    key=f"mic_{st.session_state.mic_key}"
)

# --- TEXT INPUT ---
prompt = st.chat_input("Type your message here...")

# 5. Handling Logic
# 1. ALWAYS Check Text Input First
if prompt:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process Text Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Check if the user wants a Voice Response for this text
        endpoint = "/chat/voice" if voice_mode else "/chat"
        
        if not voice_mode:
            # Standard Text-Only Streaming
            with requests.post(f"http://localhost:8000{endpoint}", json={"message": prompt}, stream=True) as r:
                for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            # Handle Text-Input-to-Voice-Output if needed, or simply standard text
            # For now, we'll keep it text-only for text input to avoid buffer confusion
            pass
    
    # CRITICAL: Reset mic key so it doesn't trigger on rerun
    st.session_state.mic_key += 1
    st.rerun()

# 2. Only check Audio if no Text prompt was sent
elif audio_bytes:
    # --- NEW SAFETY CHECK ---
    # Check if the audio data is empty or too small to be a valid recording
    if len(audio_bytes) < 1000: 
        st.warning("No clear audio detected. Please speak closer to the mic.")
    else:
        st.session_state.messages.append({"role": "user", "content": "🎤 *Voice Message Sent*"})
        
        with st.spinner("Processing voice..."):
            files = {"file": ("input.wav", audio_bytes, "audio/wav")}
            try:
                # Backend request
                response = requests.post("http://localhost:8000/chat/voice", files=files)
                
                if response.status_code == 200:
                    ai_text = response.headers.get("X-Text-Response", "Audio Response")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": ai_text, 
                        "audio": response.content
                    })
                    
                    # Increment mic_key to reset the component
                    st.session_state.mic_key += 1
                    st.rerun()
                else:
                    st.error(f"Backend Error: {response.text}")

            except requests.exceptions.ConnectionError:
                # This specifically catches the 'Connection aborted' crash
                st.error("The backend server crashed processing that audio. Try speaking again.")