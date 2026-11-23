from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import socket
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("aws-container-platform")

START_TIME = time.time()

app = FastAPI(
    title="AWS Container Platform API",
    version="0.2.0",
    description="Workload simulation, health, and runtime telemetry service for cloud & FinOps experimentation.",
)


class WorkloadRequest(BaseModel):
    iterations: int = Field(default=250_000, ge=1_000, le=5_000_000)
    tag: str = Field(default="default-batch", min_length=1, max_length=64)


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "service": "aws-container-platform",
        "version": app.version,
        "environment": os.getenv("APP_ENV", "local"),
        "host": socket.gethostname(),
    }


@app.get("/health")
def health_check():
    return {"health": "healthy", "uptime_seconds": round(time.time() - START_TIME, 2)}


@app.post("/simulate-load")
def simulate_load(payload: WorkloadRequest):
    t0 = time.perf_counter()
    acc = 0
    for i in range(payload.iterations):
        acc += (i * 7) % 13
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    if elapsed_ms > 10_000:
        raise HTTPException(status_code=504, detail="Workload simulation timed out")

    logger.info(
        f"workload_executed tag={payload.tag} iterations={payload.iterations} elapsed_ms={elapsed_ms}"
    )
    return {
        "tag": payload.tag,
        "iterations": payload.iterations,
        "checksum": acc,
        "elapsed_ms": elapsed_ms,
    }
