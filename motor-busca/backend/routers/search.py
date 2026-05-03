import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List

from algorithms import get_strategy, list_algorithms
from telemetry.setup import get_tracer
from telemetry.metrics import instruments
from opentelemetry.trace import StatusCode

router = APIRouter()
logger = logging.getLogger(__name__)


class SearchResponse(BaseModel):
    found: bool
    occurrences: int
    positions: List[int]
    execution_time_ms: float
    text_length: int
    pattern_length: int
    algorithm: str
    algorithm_label: str


ALGORITHM_LABELS = {
    "naive": "Força Bruta (Naive)",
    "rabin_karp": "Rabin-Karp",
    "kmp": "KMP (Knuth-Morris-Pratt)",
    "boyer_moore": "Boyer-Moore",
}


@router.get("/algorithms")
def get_algorithms():
    return list_algorithms()


@router.post("/search", response_model=SearchResponse)
async def search(
    file: UploadFile = File(...),
    pattern: str = Form(...),
    algorithm: str = Form(...),
):
    tracer = get_tracer()
    inst = instruments()

    with tracer.start_as_current_span("search_request") as root_span:
        root_span.set_attribute("algorithm", algorithm)
        root_span.set_attribute("pattern", pattern)

        # ── Span 1: File loading ────────────────────────────────────────────
        with tracer.start_as_current_span("load_document") as load_span:
            if not file.filename.lower().endswith(".txt"):
                raise HTTPException(status_code=400, detail="Apenas arquivos .txt são suportados.")

            content_bytes = await file.read()
            try:
                text = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = content_bytes.decode("latin-1")

            load_span.set_attribute("file.name", file.filename)
            load_span.set_attribute("file.size_bytes", len(content_bytes))
            load_span.set_attribute("document.length_chars", len(text))

        logger.info(
            f"[SEARCH START] algorithm={algorithm} N={len(text)} M={len(pattern)} pattern='{pattern[:50]}'"
        )

        # ── Span 2: Algorithm execution ─────────────────────────────────────
        with tracer.start_as_current_span("execute_algorithm") as exec_span:
            try:
                strategy = get_strategy(algorithm)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

            exec_span.set_attribute("algorithm.name", algorithm)
            exec_span.set_attribute("text.length", len(text))
            exec_span.set_attribute("pattern.length", len(pattern))

            result = strategy.execute(text, pattern)

            exec_span.set_attribute("result.found", result.found)
            exec_span.set_attribute("result.occurrences", result.occurrences)
            exec_span.set_attribute("result.execution_time_ms", result.execution_time_ms)
            exec_span.set_status(StatusCode.OK)

        # ── Span 3: Formatting result ────────────────────────────────────────
        with tracer.start_as_current_span("format_result"):
            label = ALGORITHM_LABELS.get(algorithm, algorithm)
            response = SearchResponse(
                **result.__dict__,
                algorithm_label=label,
            )

        # ── Metrics ─────────────────────────────────────────────────────────
        labels = {"algorithm": algorithm, "found": str(result.found).lower()}

        inst["search_duration"].record(result.execution_time_ms, attributes=labels)
        inst["search_requests"].add(1, attributes=labels)
        inst["document_size"].record(len(text), attributes={"algorithm": algorithm})

        logger.info(
            f"[SEARCH END] algorithm={algorithm} time_ms={result.execution_time_ms} "
            f"occurrences={result.occurrences} found={result.found}"
        )

        root_span.set_attribute("response.occurrences", result.occurrences)

    return response
