"""Main FastAPI application."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from url_shortener_auth.web.api.api import router as url_shortener_auth_router

app = FastAPI(
    docs_url="/url-shortener-auth/docs",
    redoc_url=None,
    openapi_url="/url-shortener-auth/openapi.json",
)

origins = ["http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    url_shortener_auth_router, prefix="/url-shortener-auth", tags=["url_shortener_auth"]
)


@app.get("/url-shortener-auth")
async def root():
    """Root endpoint."""
    return {"message": f"Hello from {os.getenv("HOSTNAME", default="local")}"}
