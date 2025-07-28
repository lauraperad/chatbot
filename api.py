from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from rag_engine import answer_question

# Carrega variáveis do .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN", "supertoken123")

app = FastAPI()

@app.post("/chatbot")
async def chatbot(request: Request):
    body = await request.json()
    question = body.get("message")
    token = body.get("token")

    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido.")

    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Pergunta vazia.")

    resposta = answer_question(question)
    return JSONResponse(content={"response": resposta})
