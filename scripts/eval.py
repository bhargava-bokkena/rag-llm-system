import time
import json
import httpx

API_URL = "http://127.0.0.1:8000/api/v1/ask"

TESTS = [
    {
        "question": "What does the internal knowledge base contain?",
        "expect_any": ["deployment", "CI/CD", "troubleshooting", "microservices"],
    },
    {
        "question": "List the main components of a RAG system.",
        "expect_any": ["ingestion", "chunking", "embedding", "vector", "retrieval", "synthesis"],
    },
    {
        "question": "What is the company vacation policy?",
        "expect_any": ["I don't know", "don’t know", "cannot find", "not in the context"],
    },
]


def contains_any(text: str, keywords: list[str]) -> bool:
    t = text.lower()
    return any(k.lower() in t for k in keywords)


def main():
    results = []
    with httpx.Client(timeout=60.0) as client:
        for t in TESTS:
            payload = {"question": t["question"], "top_k": 2}
            start = time.time()
            r = client.post(API_URL, json=payload)
            duration_ms = int((time.time() - start) * 1000)

            r.raise_for_status()
            data = r.json()

            ok = contains_any(data.get("answer", ""), t["expect_any"])
            top_source = (data.get("sources") or [{}])[0].get("source")

            results.append(
                {
                    "question": t["question"],
                    "ok": ok,
                    "duration_ms": duration_ms,
                    "metrics": data.get("metrics", {}),
                    "top_source": top_source,
                    "answer_preview": data.get("answer", "")[:120],
                }
            )

    passed = sum(1 for x in results if x["ok"])
    total = len(results)

    print("\n=== RAG EVAL REPORT ===")
    print(f"Passed: {passed}/{total}")
    print(f"Avg latency (ms): {sum(x['duration_ms'] for x in results)//total}")

    print("\nDetails:")
    for x in results:
        print("\n---")
        print("Q:", x["question"])
        print("OK:", x["ok"])
        print("Latency(ms):", x["duration_ms"])
        print("Stage metrics:", x["metrics"])
        print("Top source:", x["top_source"])
        print("Answer:", x["answer_preview"], "...")


if __name__ == "__main__":
    main()
