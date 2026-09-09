import os
import sys
from pathlib import Path

# Ensure the package root is on sys.path so routers can import db, shortener, etc.
sys.path.insert(0, str(Path(__file__).parent))

import db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import links, redirect

app = FastAPI(
    title="Oracle URL Shortener API",
    description="REST API for the Oracle URL shortener. Part 2 of a 5-part series.",
    version="1.0.0",
)

allowed_origins = os.environ.get("ORACLE_ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


db.init_db()

app.include_router(links.router)
app.include_router(redirect.router)
