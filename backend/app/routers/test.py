from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud
from .. import models
from ..dependencies import get_current_user
from ..schemas import SubmitAnswers, SubmitSubtopicAnswers

router = APIRouter(prefix="/test", tags=["Test"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/generate/{topic_id}")
def generate_test(topic_id: int,
                  db: Session = Depends(get_db),
                  current_user = Depends(get_current_user)):

    questions = crud.get_adaptive_questions(db, current_user.id, topic_id)

    return [
        {
            "id": q.id,
            "subtopic_id": q.subtopic_id,
            "topic_id": q.topic_id,
            "question": q.question,
            "options": {
                "a": q.option_a,
                "b": q.option_b,
                "c": q.option_c,
                "d": q.option_d,
            },
            "correct_answer": q.correct_answer,
            "difficulty": q.difficulty,
        }
        for q in questions
    ]

@router.get("/generate-subtopic/{subtopic_id}")
def generate_subtopic_test(subtopic_id: int,
                           db: Session = Depends(get_db),
                           current_user = Depends(get_current_user)):
    """Generate test questions for a specific subtopic (5 questions for practice)"""
    questions = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id
    ).limit(5).all()
    
    return [
        {
            "id": q.id,
            "subtopic_id": q.subtopic_id,
            "topic_id": q.topic_id,
            "question": q.question,
            "options": {
                "a": q.option_a,
                "b": q.option_b,
                "c": q.option_c,
                "d": q.option_d,
            },
            "correct_answer": q.correct_answer,
            "difficulty": q.difficulty,
        }
        for q in questions
    ]

@router.post("/submit-subtopic")
def submit_subtopic_test(
    request: SubmitSubtopicAnswers,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Submit test for a specific subtopic and calculate score"""
    subtopic_id = request.subtopic_id
    answers = request.answers

    # Get only the questions they answered (those with answers provided)
    question_ids = [int(qid) for qid in answers.keys()]
    questions_answered = db.query(models.Question).filter(
        models.Question.id.in_(question_ids)
    ).all()

    correct = 0
    total = len(questions_answered)  # Score out of 5 questions they answered

    # Calculate score for the 5 questions
    for q in questions_answered:
        if str(q.id) in answers and answers[str(q.id)] == q.correct_answer:
            correct += 1

    accuracy = (
        (correct / total) * 100
        if total > 0 else 0
    )

    # Save subtopic progress
    sub_progress = db.query(
        models.UserSubtopicProgress
    ).filter(
        models.UserSubtopicProgress.user_id == current_user.id,
        models.UserSubtopicProgress.subtopic_id == subtopic_id
    ).first()

    if not sub_progress:
        sub_progress = models.UserSubtopicProgress(
            user_id=current_user.id,
            subtopic_id=subtopic_id,
            attempts=0,
            time_spent=0
        )
        db.add(sub_progress)

    sub_progress.accuracy = accuracy
    sub_progress.score = correct
    sub_progress.attempts = (sub_progress.attempts or 0) + 1
    sub_progress.time_spent = (sub_progress.time_spent or 0) + 30
    sub_progress.is_completed = True

    db.commit()

    # Determine weak topics within this subtopic (if score < 70%)
    weak_areas = []
    if accuracy < 70:
        subtopic = db.query(models.Subtopic).filter(
            models.Subtopic.id == subtopic_id
        ).first()
        if subtopic:
            weak_areas.append({
                "subtopic_id": subtopic_id,
                "name": subtopic.title,
                "accuracy": round(accuracy, 2),
                "correct": correct,
                "total": total
            })

    return {
        "score": correct,
        "total": total,
        "accuracy": round(accuracy, 2),
        "weak_areas": weak_areas,
        "recommendation": f"Review this subtopic to improve your understanding. You got {accuracy:.1f}% correct!" if accuracy < 70 else "Excellent! You've mastered this subtopic!"
    }

@router.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }

@router.post("/submit")
def submit_test(
    request: SubmitAnswers,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    topic_id = request.topic_id
    answers = request.answers

    questions = db.query(models.Question).filter(
        models.Question.topic_id == topic_id
    ).all()

    correct = 0
    subtopic_scores = {}

    # ----------------------------
    # Calculate Scores
    # ----------------------------
    for q in questions:

        if q.subtopic_id not in subtopic_scores:
            subtopic_scores[q.subtopic_id] = {
                "correct": 0,
                "total": 0
            }

        subtopic_scores[q.subtopic_id]["total"] += 1

        if str(q.id) in answers and answers[str(q.id)] == q.correct_answer:
            correct += 1
            subtopic_scores[q.subtopic_id]["correct"] += 1

    total = len(questions)

    accuracy = (
        (correct / total) * 100
        if total > 0 else 0
    )

    # ----------------------------
    # Save Topic Progress
    # ----------------------------
    topic_progress = db.query(
        models.UserTopicProgress
    ).filter(
        models.UserTopicProgress.user_id == current_user.id,
        models.UserTopicProgress.topic_id == topic_id
    ).first()

    if not topic_progress:
        topic_progress = models.UserTopicProgress(
            user_id=current_user.id,
            topic_id=topic_id,
            accuracy=accuracy,
            last_score=correct
        )
        db.add(topic_progress)

    topic_progress.accuracy = accuracy
    topic_progress.last_score = correct

    # ----------------------------
    # Save Subtopic Progress
    # ----------------------------
    for subtopic_id, data in subtopic_scores.items():

        sub_accuracy = (
            data["correct"] / data["total"]
        ) * 100 if data["total"] > 0 else 0

        sub_progress = db.query(
            models.UserSubtopicProgress
        ).filter(
            models.UserSubtopicProgress.user_id == current_user.id,
            models.UserSubtopicProgress.subtopic_id == subtopic_id
        ).first()

        if not sub_progress:
            sub_progress = models.UserSubtopicProgress(
                user_id=current_user.id,
                subtopic_id=subtopic_id,
                attempts=0,
                time_spent=0
            )
            db.add(sub_progress)

        sub_progress.accuracy = sub_accuracy
        sub_progress.score = data["correct"]

        # ✅ Safe attempts increment
        sub_progress.attempts = (
            sub_progress.attempts or 0
        ) + 1

        sub_progress.time_spent = (
            sub_progress.time_spent or 0
        ) + 30  # dummy time

        sub_progress.is_completed = True

    db.commit()

    # Find weak areas (< 70% accuracy)
    weak_areas = []
    for subtopic_id, data in subtopic_scores.items():
        sub_accuracy = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0
        
        if sub_accuracy < 70:
            subtopic = db.query(models.Subtopic).filter(models.Subtopic.id == subtopic_id).first()
            if subtopic:
                weak_areas.append({
                    "subtopic_id": subtopic_id,
                    "name": subtopic.title,
                    "accuracy": round(sub_accuracy, 2),
                    "correct": data["correct"],
                    "total": data["total"]
                })

    return {
        "score": correct,
        "total": total,
        "accuracy": accuracy,
        "subtopic_scores": subtopic_scores,
        "weak_areas": weak_areas,
        "recommendation": f"Review weak areas to improve your understanding. You got {accuracy:.1f}% correct!" if weak_areas else "Great job! You've mastered this topic!"
    }