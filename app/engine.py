import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def create_white_label_agent(client_data_path: str, system_persona: str):
    # 1. Load document context
    if os.path.isdir(client_data_path):
        loader = DirectoryLoader(client_data_path, glob="**/*.txt")
    else:
        loader = TextLoader(client_data_path)
    
    documents = loader.load()
    
    # 2. RAG pipeline setup
    # Using Llama 3 as specified in your tech stack
    embeddings = OllamaEmbeddings(model="llama3")
    vectorstore = DocArrayInMemorySearch.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    
    llm = ChatOllama(model="llama3")
    
    # 3. Custom persona prompt
    custom_prompt = PromptTemplate(
        template=system_persona + "\n\nContext: {context}\nQuestion: {question}",
        input_variables=["context", "question"]
    )

    # 4. Modern LCEL Chain (Replaces legacy ConversationalRetrievalChain)
    # This bypasses the Pydantic v1 issues with Python 3.14
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | custom_prompt
        | llm
        | StrOutputParser()
    )

    return chain