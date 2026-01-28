"""
Prmpt Backend - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import judge, levels, user
from app.core.config import settings

app = FastAPI(
    title="Prmpt API",
    description="Backend API for Prmpt - Gamified Prompt Engineering Academy",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(judge.router, prefix="/api", tags=["Judge"])
app.include_router(levels.router, prefix="/api", tags=["Levels"])
app.include_router(user.router, prefix="/api", tags=["User"])


@app.get("/")
async def root():
    return {"message": "Prmpt API", "status": "healthy"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
