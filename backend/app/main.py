from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, roadmap
from app.database import engine
from app import models
from app.routers import analytics
from app.routers import test
from app.routers import adaptive
from app.database import Base, engine
from app.routers import ai_routes
from app.routers import chat

Base.metadata.create_all(bind=engine)


app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
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

@app.get("/")
def root():
    return {"message": "NDA Prep API Running 🚀"}