import os
import gradio as gr
from dotenv import load_dotenv
from rag_engine import answer_question

# Carrega variáveis de ambiente do .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN", "supertoken123")

def ask_question_api(question, token):
    if token != API_TOKEN:
        return {"answer": None, "error": "❌ Token inválido."}

    if not question.strip():
        return {"answer": None, "error": "⚠️ Nenhuma pergunta foi fornecida."}

    answer = answer_question(question)
    return {"answer": answer, "error": None}

with gr.Blocks(title="API de Perguntas com Token") as demo:
    gr.Markdown("### 🤖 API RAG com Token de Autenticação")
    token = gr.Text(label="🔐 Token", type="password")
    question = gr.Textbox(label="❓ Pergunta", placeholder="Digite sua pergunta aqui...")
    output = gr.JSON(label="📤 Resposta JSON")
    gr.Button("Enviar").click(fn=ask_question_api, inputs=[question, token], outputs=output)

if __name__ == "__main__":
    demo.launch()
