from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from telemetry.setup import setup_telemetry
from routers import search

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_telemetry()
    yield

app = FastAPI(
    title="Motor de Busca em Documentos",
    description="Substring search engine with OpenTelemetry observability",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
