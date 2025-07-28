import os
from dotenv import load_dotenv
from huggingface_hub import login
from utils import load_vectorstore
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Carrega variáveis do .env
load_dotenv()
login(token=os.getenv("HUGGINGFACE_HUB_TOKEN"))

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype="auto"
)

rag_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=500)

vectorstore_path = os.getenv("VECTORSTORE_PATH", "data/vectorstore")
vectorstore = load_vectorstore(vectorstore_path)

def build_prompt(context: str, question: str) -> str:
    return (
        f"[INST] Responda com base no contexto abaixo.\n\n"
        f"Contexto:\n{context}\n\n"
        f"Pergunta: {question}\nResposta: [/INST]"
    )

def answer_question(question: str) -> str:
    if vectorstore is None:
        return "Erro: vectorstore não carregado corretamente."

    docs = vectorstore.similarity_search(question, k=3)
    if not docs:
        return "Nenhuma informação relevante encontrada no contexto."

    context = "\n".join([doc.page_content for doc in docs])[:3000]
    prompt = build_prompt(context, question)

    try:
        resposta = rag_pipeline(prompt)[0]['generated_text']
        return resposta.replace(prompt, "").strip()
    except Exception as e:
        return f"Erro ao gerar resposta com modelo local: {str(e)}"
