from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import APP_NAME, APP_VERSION, FRONTEND_URL
from backend.routes import router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered legal document generation API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:8502",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }

app.include_router(router)