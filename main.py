from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from rag_engine import answer_question

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "supertoken123")

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    user_message = data.get("text", "")
    token = data.get("token", "")

    if token != API_TOKEN:
        return JSONResponse(content={"text": "❌ Token inválido."}, status_code=403)

    if not user_message.strip():
        return JSONResponse(content={"text": "⚠️ Nenhuma pergunta foi enviada."})

    resposta = answer_question(user_message)
    return JSONResponse(content={"text": resposta})
