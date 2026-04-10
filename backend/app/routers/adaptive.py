from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud
from ..dependencies import get_current_user

router = APIRouter(prefix="/adaptive", tags=["Adaptive"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/questions/{topic_id}")
def get_questions(topic_id: int,
                  db: Session = Depends(get_db),
                  current_user = Depends(get_current_user)):

    questions = crud.get_adaptive_questions(db, current_user.id, topic_id)
    
    return [
        {
            "id": q.id,
            "subtopic_id": q.subtopic_id,
            "topic_id": q.topic_id,
            "text": q.text,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "difficulty": q.difficulty,
        }
        for q in questions
    ]