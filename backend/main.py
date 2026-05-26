from fastapi import FastAPI
from pydantic import BaseModel

from backend.rag_service import get_rag_answer

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Agentic AI RAG API is running"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return get_rag_answer(request.question)