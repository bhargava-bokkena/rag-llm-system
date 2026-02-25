import time
import uuid
import logging
from fastapi import FastAPI, Request

from app.api.v1.routes import router as v1_router
from app.core.logging_config import setup_logging
from app.rag.guards import assert_vectorstore_compatible

logger = logging.getLogger("app")


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title="RAG / LLM System")
    app.include_router(v1_router, prefix="/api/v1")

    # Fail fast if Chroma was built with a different embedding model
    assert_vectorstore_compatible("documents")

    @app.middleware("http")
    async def add_trace_and_timing(request: Request, call_next):
        trace_id = request.headers.get("x-trace-id") or str(uuid.uuid4())
        start = time.time()

        request.state.trace_id = trace_id

        logger.info(
            f"{request.method} {request.url.path} start",
            extra={"trace_id": trace_id},
        )

        response = await call_next(request)

        duration_ms = int((time.time() - start) * 1000)
        response.headers["x-trace-id"] = trace_id
        response.headers["x-duration-ms"] = str(duration_ms)

        logger.info(
            f"{request.method} {request.url.path} done status={response.status_code} duration_ms={duration_ms}",
            extra={"trace_id": trace_id},
        )
        return response

    return app


app = create_app()
