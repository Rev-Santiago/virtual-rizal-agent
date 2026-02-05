# 🇵🇭 Virtual Rizal Agent: A Historical Digital Twin

The **Virtual Rizal Agent** is a generative AI project that brings Dr. Jose Rizal, the national hero of the Philippines, to life. Built using a **Retrieval-Augmented Generation (RAG)** architecture, this agent allows users to engage in intellectual and philosophical dialogue with a "digital twin" that embodies Rizal's sophisticated tone, multilingual background, and historical insights.

---

## 🛠️ The Tech Stack

This project is built with industry-standard tools to ensure local performance and high-quality AI orchestration:

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - For a high-performance, asynchronous backend.
* **Orchestration:** [LangChain](https://www.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/) - To manage stateful conversations and RAG logic.
* **Local LLM:** [Ollama](https://ollama.com/) (running **Llama 3**) - Ensures privacy and low-latency responses by running the brain locally.
* **Environment:** Python 3.10+ with a modular directory structure.

---

## 🧠 Key Features

- **Intellectual Persona:** The agent is guided by a complex system prompt that maintains Rizal's gentlemanly decorum and "Ilustrado" perspective.
- **RAG Brain:** Instead of relying on general model knowledge, the agent "reads" from a curated knowledge base of Rizal's life, his novels (*Noli Me Tángere* & *El Filibusterismo*), and his final poetry.
- **Multi-lingual Awareness:** Capable of understanding and responding in Tagalog, Spanish, and English.
- **Modular Architecture:** Separates API routes from the AI engine for easier scalability.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have [Ollama](https://ollama.com/) installed and the Llama 3 model downloaded:
```terminal
ollama pull llama3
```

### 2. Installation
Clone the repository and set up the environment:
```terminal
    git clone [https://github.com/Rev-Santiago/virtual-rizal-agent.git](https://github.com/Rev-Santiago/virtual-rizal-agent.git)
    cd virtual-rizal-agent
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    pip install -r requirements.txt
```

### 3. Run the Agent
Start the FastAPI server:
```terminal
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000

## 📂 Project Structure
```Plaintext
virtual-rizal-agent/
├── app/
│   ├── main.py      # API Endpoints
│   ├── engine.py    # LangChain & RAG Logic
│   └── utils.py     # Document loaders
├── data/
│   └── rizal_context.txt # The "Source of Truth"
├── requirements.txt
└── README.md
```