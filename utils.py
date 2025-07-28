import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Modelo de embeddings local da Hugging Face
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def load_vectorstore(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Vectorstore não encontrado em {path}")
    return FAISS.load_local(path, embeddings)

def ingest_documents():
    data_path = Path("data")
    vectorstore_path = Path("data/vectorstore")
    docs = []

    for file in data_path.glob("**/*"):
        if file.suffix == ".pdf":
            docs.extend(PyPDFLoader(str(file)).load())
        elif file.suffix == ".docx":
            docs.extend(Docx2txtLoader(str(file)).load())
        elif file.suffix == ".txt":
            docs.extend(TextLoader(str(file)).load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(str(vectorstore_path))
