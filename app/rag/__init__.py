import time
import logging
from typing import Any, Dict
from app.rag.retrieval import retrieve, build_prompt
from app.rag.llm import chat

logger = logging.getLogger("rag")

def rag_answer(question: str, k: int = 4) -> Dict[str, Any]:
    t0 = time.time()
    contexts = retrieve(question, k=k)
    t_retrieve = int((time.time() - t0) * 1000)

    t1 = time.time()
    prompt = build_prompt(question, contexts)
    answer = chat(prompt)
    t_llm = int((time.time() - t1) * 1000)

    logger.info(
        f"rag_answer k={k} retrieve_ms={t_retrieve} llm_ms={t_llm}",
        extra={"trace_id": "na"},
    )

    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "metrics": {"retrieve_ms": t_retrieve, "llm_ms": t_llm, "total_ms": int((time.time()-t0)*1000)},
    }
