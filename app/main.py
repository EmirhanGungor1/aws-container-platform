from fastapi import FastAPI
import os

app = FastAPI(title="AWS Container Platform API")

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "service": "aws-container-platform",
        "environment": os.getenv("APP_ENV", "local")
    }

@app.get("/health")
def health_check():
    return {"health": "healthy"}
