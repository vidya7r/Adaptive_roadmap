import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from parent directory (backend/)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, roadmap
from .database import engine
from . import models
from .routers import analytics
from .routers import test
from .routers import adaptive
from .database import Base, engine
from .routers import ai_routes
from .routers import chat
from .routers import resources

Base.metadata.create_all(bind=engine)


app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
        "http://127.0.0.1:5177",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(analytics.router)
app.include_router(test.router)
app.include_router(adaptive.router)
app.include_router(ai_routes.router)
app.include_router(chat.router)
app.include_router(roadmap.router)
app.include_router(resources.router)

@app.get("/")
def root():
    return {"message": "NDA Prep API Running 🚀"}