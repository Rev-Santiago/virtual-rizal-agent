import os
import config # Import config
from operator import itemgetter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def create_white_label_agent(client_data_path: str, system_persona: str):
    if os.path.isdir(client_data_path):
        loader = DirectoryLoader(client_data_path, glob="**/*.txt")
    else:
        loader = TextLoader(client_data_path)
    
    documents = loader.load()
    
    # Updated: Use config.OLLAMA_BASE_URL
    embeddings = OllamaEmbeddings(
        model=config.MODEL_NAME, 
        base_url=config.OLLAMA_BASE_URL
    )
    vectorstore = DocArrayInMemorySearch.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    
    # Updated: Use config.OLLAMA_BASE_URL
    llm = ChatOllama(
        model=config.MODEL_NAME, 
        base_url=config.OLLAMA_BASE_URL
    )
    
    custom_prompt = ChatPromptTemplate.from_messages([
        ("system", system_persona + "\n\nContext: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])

    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | custom_prompt
        | llm
        | StrOutputParser()
    )

    return chain