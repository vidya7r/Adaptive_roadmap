from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, roadmap
from .routers import resources
from .database import engine
from . import models
from .routers import analytics
from .routers import test
from .routers import adaptive
from .database import Base, engine
from .routers import ai_routes
from .routers import chat

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
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
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