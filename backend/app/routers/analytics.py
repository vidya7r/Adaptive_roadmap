from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# 🎯 Weak Subtopics API
# --------------------------------------------------

@router.get("/weak-subtopics")
def get_weak_subtopics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    weak_subtopics = db.query(
        models.UserSubtopicProgress
    ).filter(
        models.UserSubtopicProgress.user_id == current_user.id,
        models.UserSubtopicProgress.accuracy < 60
    ).order_by(
        models.UserSubtopicProgress.accuracy.asc()
    ).all()

    return [
        {
            "id": item.id,
            "user_id": item.user_id,
            "subtopic_id": item.subtopic_id,
            "accuracy": item.accuracy,
            "attempts": item.attempts,
            "correct_answers": item.correct_answers,
            "subtopic_title": item.subtopic.title if item.subtopic else "Unknown"
        }
        for item in weak_subtopics
    ]

# --------------------------------------------------
# 📝 Test History API
# --------------------------------------------------

@router.get("/test-history")
def get_test_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    tests = db.query(
        models.TopicTest
    ).filter(
        models.TopicTest.user_id == current_user.id
    ).order_by(
        models.TopicTest.created_at.desc()
    ).all()

    return [
        {
            "id": test.id,
            "user_id": test.user_id,
            "topic_id": test.topic_id,
            "score": test.score,
            "total": test.total,
            "created_at": test.created_at.isoformat() if test.created_at else None,
            "topic_title": test.topic.title if test.topic else "Unknown"
        }
        for test in tests
    ]

@router.get("/recommendations")
def get_recommendations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Weak subtopics (<60%)
    weak = db.query(
        models.UserSubtopicProgress
    ).filter(
        models.UserSubtopicProgress.user_id == current_user.id,
        models.UserSubtopicProgress.accuracy < 60
    ).order_by(
        models.UserSubtopicProgress.accuracy.asc()
    ).all()

    # Strong subtopics (>=60%)
    strong = db.query(
        models.UserSubtopicProgress
    ).filter(
        models.UserSubtopicProgress.user_id == current_user.id,
        models.UserSubtopicProgress.accuracy >= 60
    ).order_by(
        models.UserSubtopicProgress.accuracy.desc()
    ).all()

    return {
        "focus_now": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "subtopic_id": item.subtopic_id,
                "accuracy": item.accuracy,
                "attempts": item.attempts,
                "correct_answers": item.correct_answers,
                "subtopic_title": item.subtopic.title if item.subtopic else "Unknown"
            }
            for item in weak
        ],
        "revise_later": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "subtopic_id": item.subtopic_id,
                "accuracy": item.accuracy,
                "attempts": item.attempts,
                "correct_answers": item.correct_answers,
                "subtopic_title": item.subtopic.title if item.subtopic else "Unknown"
            }
            for item in strong
        ]
    }

# --------------------------------------------------
# 📊 TOPIC MASTERY TRACKER
# --------------------------------------------------

@router.get("/topic-mastery")
def get_topic_mastery(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Total topics
    total_topics = db.query(
        models.Topic
    ).count()

    # Completed topics
    completed_topics = db.query(
        models.UserTopicProgress
    ).filter(
        models.UserTopicProgress.user_id == current_user.id,
        models.UserTopicProgress.is_completed == True
    ).count()

    # In-progress topics
    in_progress_topics = db.query(
        models.UserTopicProgress
    ).filter(
        models.UserTopicProgress.user_id == current_user.id,
        models.UserTopicProgress.is_completed == False
    ).count()

    # Not started topics
    not_started_topics = (
        total_topics
        - completed_topics
        - in_progress_topics
    )

    return {
        "total_topics": total_topics,
        "completed_topics": completed_topics,
        "in_progress_topics": in_progress_topics,
        "not_started_topics": not_started_topics
    }