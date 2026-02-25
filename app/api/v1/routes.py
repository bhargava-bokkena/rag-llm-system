from fastapi import APIRouter
from pydantic import BaseModel
from app.rag import rag_answer

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}


class AskRequest(BaseModel):
    question: str
    top_k: int = 4


@router.post("/ask")
def ask(payload: AskRequest):
    result = rag_answer(payload.question, k=payload.top_k)
    return {
        "question": result["question"],
        "answer": result["answer"],
        "metrics": result["metrics"],
        "sources": [
            {"source": c["metadata"].get("source", "unknown"), "distance": c["distance"]}
            for c in result["contexts"]
        ],
    }
