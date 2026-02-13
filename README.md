# 🤖 White-Label RAG Agent (Virtual Rizal & Business Support)

The **Virtual Rizal Agent** has evolved into a modular, containerized AI platform. It is designed to be "white-labeled" for different personas, allowing you to instantly switch between a **Historical Digital Twin** (Dr. Jose Rizal) and a **Professional Business Consultant** (Modern Real Estate).

Built using a **Retrieval-Augmented Generation (RAG)** architecture, this agent uses **Llama 3 (via Ollama)** for local inference and **LangChain** for orchestration.

---

## 🛠️ The Tech Stack

This project is built with industry-standard tools to ensure local performance and high-quality AI orchestration:

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - For a high-performance, asynchronous backend.
* **Orchestration:** [LangChain](https://www.langchain.com/) - To manage stateful conversations and RAG logic.
* **Local LLM:** [Ollama](https://ollama.com/) (running **Llama 3**) - Ensures privacy and low-latency responses by running the brain locally.
* **Containerization:** [Docker](https://www.docker.com/) - Ensures the app runs consistently on any machine.
* **Environment:** Python 3.11+ with a modular directory structure.

---

## 🌟 Key Features

- **Persona Switching:** Instantly swap between "Jose Rizal" (Historical) and "Modern Real Estate" (Business) using the built-in launcher.
- **Hallucination Guardrails:** Strict system prompts ensure the AI only answers from the provided data and refuses to make up facts.
- **Conversational Memory:** The agent remembers context across turns (e.g., "How much is *it*?").
- **Multi-lingual Awareness:** Capable of understanding and responding in Tagalog, Spanish, and English.
- **Dockerized Deployment:** Runs seamlessly in a container, communicating with your local Ollama instance.

---

## 🚀 Getting Started (Docker)

**Prerequisite:** Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running.

### 1. Installation
Clone the repository and enter the directory:
```bash
git clone [https://github.com/Rev-Santiago/virtual-rizal-agent.git](https://github.com/Rev-Santiago/virtual-rizal-agent.git)
cd virtual-rizal-agent
```
### 2. Select Your Persona
Run the configuration script to choose which agent you want to run:
```Bash
python launch.py
# Select Option 1 (Rizal) or Option 2 (Real Estate)
```

### 3. Start the Container
Build and run the agent. This links the container to your local Ollama instance.
```Bash
docker-compose up --build
```
The API will be available at http://localhost:8000

### 4. Chat with the Agent
In a separate terminal, launch the test client to talk to your agent:
```Bash
python test_client.py
# Type '/clear' to reset conversation memory
```

---

## 🛠️ Configuration & Customization
### Adding a New Client
    To add a new business or persona (e.g., "Tech Support"):
#### 1. Create Data: Add a text file to data/ (e.g., data/tech_support.txt).
#### 2. Update Launcher: Edit launch.py to add a new menu option:
```Python
    elif choice == "3":
        update_env(
            "Tech Support",
            "data/tech_support.txt",
            "You are a tech support agent. Rules: Answer only from the Context. If unknown, say 'I don't know'."
        )
```

#### 3. Restart: Run python launch.py -> 3, then docker-compose up --build.

### Adjusting Guardrails
    Modify the SYSTEM_PROMPT in launch.py to tighten or loosen constraints.

- **Strict**: "If the answer is not in Context, say 'I do not know'."

- **Creative**: "You may use general knowledge to supplement the Context."

---

## 📂 Project Structure
```Plaintext
virtual-rizal-agent/
├── app/
│   ├── main.py          # FastAPI Application & Streaming Logic
│   └── engine.py        # LangChain RAG Chain (The "Brain")
├── data/
│   ├── persona_context.txt  # Knowledge Base for Rizal
│   └── real_estate_faqs.txt # Knowledge Base for Real Estate
├── launch.py            # CLI Tool to switch personas (Updates .env)
├── test_client.py       # Terminal Chat Interface with Memory Support
├── docker-compose.yml   # Container Orchestration
├── Dockerfile           # Docker Build Instructions
├── .env                 # Active Configuration (Managed by launch.py)
├── config.py            # Bridges .env to code
└── requirements.txt     # Python Dependencies
```