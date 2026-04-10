from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models
from ..dependencies import get_current_user

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


# --------------------------------------------------
# 📊 COMPREHENSIVE ANALYTICS DASHBOARD
# --------------------------------------------------

@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get overall user analytics summary"""
    try:
        # Get completed subtopics (tests taken)
        completed_subtopics = db.query(
            models.UserSubtopicProgress
        ).filter(
            models.UserSubtopicProgress.user_id == current_user.id,
            models.UserSubtopicProgress.is_completed == True
        ).all()
        
        total_tests = len(completed_subtopics)
        
        # Calculate average accuracy
        avg_accuracy = 0
        if completed_subtopics:
            avg_accuracy = sum([p.accuracy or 0 for p in completed_subtopics]) / total_tests
        
        # Calculate total time spent
        total_time_spent = sum([p.time_spent or 0 for p in completed_subtopics])
        
        # Get all answered questions count
        total_questions_answered = sum([p.attempts for p in completed_subtopics])
        
        return {
            "totalTests": total_tests,
            "totalQuestionsAnswered": total_questions_answered,
            "averageAccuracy": round(avg_accuracy, 1),
            "averageScore": round(avg_accuracy, 1),
            "totalTimeSpent": int(total_time_spent),
            "streakDays": 5,  # Simplified for now
        }
    except Exception as e:
        print(f"Error in get_analytics_overview: {e}")
        return {
            "totalTests": 0,
            "totalQuestionsAnswered": 0,
            "averageAccuracy": 0,
            "averageScore": 0,
            "totalTimeSpent": 0,
            "streakDays": 0,
        }


@router.get("/topics-performance")
def get_topics_performance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get performance for each topic the user has interacted with"""
    try:
        progress_list = db.query(
            models.UserSubtopicProgress
        ).filter(
            models.UserSubtopicProgress.user_id == current_user.id
        ).all()
        
        topics_performance = []
        
        for p in progress_list:
            if p.subtopic_id:
                subtopic = db.query(models.Subtopic).filter(
                    models.Subtopic.id == p.subtopic_id
                ).first()
                
                if subtopic and p.attempts > 0:
                    accuracy = p.accuracy or 0
                    
                    # Determine status and color
                    if accuracy >= 85:
                        status = "Mastered"
                        color = "#4CAF50"
                    elif accuracy >= 70:
                        status = "Good" if accuracy < 80 else "Excellent"
                        color = "#66BB6A" if accuracy < 80 else "#4CAF50"
                    elif accuracy >= 50:
                        status = "Needs Work"
                        color = "#FFC107"
                    else:
                        status = "Weak"
                        color = "#F44336"
                    
                    topics_performance.append({
                        "name": subtopic.name,
                        "accuracy": round(accuracy, 1),
                        "tests": p.attempts,
                        "status": status,
                        "color": color
                    })
        
        # Sort by accuracy descending
        topics_performance.sort(key=lambda x: x["accuracy"], reverse=True)
        
        return {"topicsMastery": topics_performance}
    except Exception as e:
        print(f"Error in get_topics_performance: {e}")
        return {"topicsMastery": []}


@router.get("/summary")
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get complete analytics dashboard data"""
    try:
        overview_data = get_analytics_overview(db=db, current_user=current_user)
        topics_data = get_topics_performance(db=db, current_user=current_user)
        
        # Get recommendations
        weak_subtopics = db.query(
            models.UserSubtopicProgress
        ).filter(
            models.UserSubtopicProgress.user_id == current_user.id,
            models.UserSubtopicProgress.accuracy < 70
        ).order_by(
            models.UserSubtopicProgress.accuracy.asc()
        ).all()
        
        recommendations = []
        
        # Add weak topic recommendations
        for p in weak_subtopics[:2]:
            if p.subtopic_id:
                subtopic = db.query(models.Subtopic).filter(
                    models.Subtopic.id == p.subtopic_id
                ).first()
                if subtopic:
                    recommendations.append(f"Focus on {subtopic.name} ({p.accuracy}% accuracy)")
        
        if len(topics_data["topicsMastery"]) > 0:
            recommendations.append(f"Great work on {topics_data['topicsMastery'][0]['name']}! Keep it up!")
        
        recommendations.append("Complete more tests to unlock advanced features")
        
        # Generate mock timeline
        progress_timeline = [
            {"date": "2024-01-15", "score": 65, "accuracy": 65, "testType": "Practice"},
            {"date": "2024-01-16", "score": 72, "accuracy": 72, "testType": "Adaptive"},
            {"date": "2024-01-17", "score": 68, "accuracy": 68, "testType": "Practice"},
            {"date": "2024-01-18", "score": 78, "accuracy": 78, "testType": "Adaptive"},
            {"date": "2024-01-19", "score": 82, "accuracy": 82, "testType": "Practice"},
        ]
        
        return {
            "overallStats": overview_data,
            "topicsMastery": topics_data["topicsMastery"],
            "progressTimeline": progress_timeline,
            "recommendations": recommendations[:4]
        }
    except Exception as e:
        print(f"Error in get_analytics_summary: {e}")
        return {
            "overallStats": {},
            "topicsMastery": [],
            "progressTimeline": [],
            "recommendations": []
        }