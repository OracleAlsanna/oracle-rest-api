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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

db.init_db()

app.include_router(links.router)
app.include_router(redirect.router)
