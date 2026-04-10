from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import SessionLocal
from .. import crud, models
from ..dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["Content"])


# Pydantic models for request validation
class ProgressUpdate(BaseModel):
    status: str

    class Config:
        json_schema_extra = {
            "example": {"status": "done"}
        }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Keep track of modules mapping (NDA structure)
MODULES = {
    1: {"id": 1, "title": "Mathematics", "icon": "🔢"},
    2: {"id": 2, "title": "Physics", "icon": "⚛️"},
    3: {"id": 3, "title": "Chemistry", "icon": "🧪"},
    4: {"id": 4, "title": "General Science", "icon": "🔬"},
    5: {"id": 5, "title": "History", "icon": "📜"},
    6: {"id": 6, "title": "Geography", "icon": "🌍"},
    7: {"id": 7, "title": "Current Affairs", "icon": "📰"},
    8: {"id": 8, "title": "SSB Interview", "icon": "👥"},
}

# Sections mapping
SECTIONS = {
    1: {
        "id": 1,
        "title": "Written",
        "description": "Written Examination - Mathematics, English, General Knowledge"
    },
    2: {
        "id": 2,
        "title": "SSB",
        "description": "Service Selection Board - Interview & Assessment"
    }
}

# Modules per section
SECTION_MODULES = {
    1: [1, 2, 3, 4, 5, 6, 7],  # Written exam modules
    2: [8]  # SSB module
}


@router.get("/sections")
def get_sections():
    """Get all exam sections (Written, SSB)"""
    return {
        "sections": list(SECTIONS.values())
    }


@router.get("/modules")
def get_modules(section_id: int = None):
    """Get modules, optionally filtered by section"""
    if section_id is None:
        return list(MODULES.values())
    
    if section_id not in SECTION_MODULES:
        raise HTTPException(status_code=404, detail=f"Section {section_id} not found")
    
    module_ids = SECTION_MODULES[section_id]
    return {
        "modules": [MODULES[mid] for mid in module_ids if mid in MODULES]
    }


@router.get("/subtopics/all")
def get_all_subtopics(db: Session = Depends(get_db)):
    """Get all subtopics from database"""
    try:
        subtopics = db.query(models.Subtopic).all()
        return [
            {
                "id": s.id,
                "title": s.title,
                "topic_id": s.topic_id,
                "description": s.description,
            }
            for s in subtopics
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/topics")
def get_all_topics(db: Session = Depends(get_db)):
    """Get all topics from database"""
    try:
        topics = db.query(models.Topic).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "module_id": t.module_id,
                "subtopics": [
                    {
                        "id": st.id,
                        "name": st.title,
                        "description": st.description,
                        "question_count": len(st.questions) if st.questions else 0,
                        "is_completed": False,
                        "is_weak": False,
                    }
                    for st in (t.subtopics if t.subtopics else [])
                ]
            }
            for t in topics
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/topics/{module_id}")
def get_topics_by_module(module_id: int, db: Session = Depends(get_db)):
    """Get topics for a specific module with their subtopics"""
    try:
        topics = db.query(models.Topic).filter(
            models.Topic.module_id == module_id
        ).all()
        
        if not topics:
            raise HTTPException(status_code=404, detail=f"No topics found for module {module_id}")
        
        return [
            {
                "id": t.id,
                "title": t.title,
                "module_id": t.module_id,
                "subtopics": [
                    {
                        "id": st.id,
                        "title": st.title,
                        "description": st.description,
                        "question_count": len(st.questions) if st.questions else 0,
                        "is_completed": False,
                    }
                    for st in (t.subtopics if t.subtopics else [])
                ]
            }
            for t in topics
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/subtopics/{topic_id}")
def get_subtopics_by_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get subtopics for a specific topic"""
    try:
        subtopics = db.query(models.Subtopic).filter(
            models.Subtopic.topic_id == topic_id
        ).all()
        
        if not subtopics:
            raise HTTPException(status_code=404, detail=f"No subtopics found for topic {topic_id}")
        
        return [
            {
                "id": s.id,
                "title": s.title,
                "topic_id": s.topic_id,
                "description": s.description,
            }
            for s in subtopics
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/subtopic/{subtopic_id}")
def get_subtopic(subtopic_id: int, db: Session = Depends(get_db)):
    """Get a single subtopic with its description and questions"""
    try:
        subtopic = db.query(models.Subtopic).filter(
            models.Subtopic.id == subtopic_id
        ).first()
        
        if not subtopic:
            raise HTTPException(status_code=404, detail=f"Subtopic {subtopic_id} not found")
        
        # Get question count
        question_count = db.query(models.Question).filter(
            models.Question.subtopic_id == subtopic_id
        ).count()
        
        return {
            "id": subtopic.id,
            "title": subtopic.title,
            "topic_id": subtopic.topic_id,
            "description": subtopic.description,
            "question_count": question_count,
            "has_explanation": bool(subtopic.description),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/questions/{subtopic_id}")
def get_questions(subtopic_id: int, db: Session = Depends(get_db)):
    """Get questions for a subtopic"""
    try:
        questions = db.query(models.Question).filter(
            models.Question.subtopic_id == subtopic_id
        ).all()
        
        if not questions:
            raise HTTPException(
                status_code=404, 
                detail=f"No questions found for subtopic {subtopic_id}. Generate them first."
            )
        
        return [
            {
                "id": q.id,
                "subtopic_id": q.subtopic_id,
                "text": q.text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "difficulty": q.difficulty,
            }
            for q in questions
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/analytics/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get overall dashboard statistics"""
    try:
        # Count statistics
        total_topics = db.query(models.Topic).count()
        total_subtopics = db.query(models.Subtopic).count()
        subtopics_with_description = db.query(models.Subtopic).filter(
            models.Subtopic.description.isnot(None)
        ).count()
        total_questions = db.query(models.Question).count()
        
        # Get questions by difficulty
        easy_count = db.query(models.Question).filter(
            models.Question.difficulty == "easy"
        ).count()
        medium_count = db.query(models.Question).filter(
            models.Question.difficulty == "medium"
        ).count()
        hard_count = db.query(models.Question).filter(
            models.Question.difficulty == "hard"
        ).count()
        
        return {
            "total_topics": total_topics,
            "total_subtopics": total_subtopics,
            "subtopics_with_ai_explanations": subtopics_with_description,
            "total_questions": total_questions,
            "questions_by_difficulty": {
                "easy": easy_count,
                "medium": medium_count,
                "hard": hard_count,
            },
            "system_status": {
                "database": "connected",
                "ai_explanations": f"{subtopics_with_description}/{total_subtopics} complete",
                "question_generation": f"{total_questions} questions generated",
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/topics/{topic_id}")
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get single topic with subtopics"""
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        return {"error": "Topic not found"}
    
    subtopics = db.query(models.Subtopic).filter(
        models.Subtopic.topic_id == topic_id
    ).all()
    
    return {
        "id": topic.id,
        "title": topic.title,
        "module_id": topic.module_id,
        "subtopics": [
            {
                "id": s.id,
                "title": s.title,
                "topic_id": s.topic_id,
                "description": s.description,
            }
            for s in subtopics
        ]
    }

@router.get("/topics/{topic_id}/subtopics")
def get_subtopics(topic_id: int, db: Session = Depends(get_db)):
    """Get subtopics for a topic"""
    return crud.get_subtopics_by_topic(db, topic_id)

@router.get("/subtopic/{subtopic_id}")
def get_subtopic(subtopic_id: int, db: Session = Depends(get_db)):
    """Get single subtopic with description"""
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == subtopic_id
    ).first()
    
    if not subtopic:
        return {"error": "Subtopic not found"}
    
    return {
        "id": subtopic.id,
        "title": subtopic.title,
        "description": subtopic.description,
        "topic_id": subtopic.topic_id
    }

@router.get("/modules")
def get_modules(db: Session = Depends(get_db)):
    """Get distinct modules/subjects"""
    # Get unique module_ids and their first topic to get the module name
    topics = db.query(models.Topic).all()
    
    # Group topics by module_id
    modules_dict = {}
    for topic in topics:
        if topic.module_id not in modules_dict:
            modules_dict[topic.module_id] = {
                "id": topic.module_id,
                "name": f"Module {topic.module_id}",
                "topics": []
            }
        modules_dict[topic.module_id]["topics"].append({
            "id": topic.id,
            "title": topic.title
        })
    
    return list(modules_dict.values())


@router.get("/subtopic/{subtopic_id}/progress")
def get_subtopic_progress(
    subtopic_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get subtopic progress for current user"""
    try:
        progress = db.query(models.UserSubtopicProgress).filter(
            models.UserSubtopicProgress.user_id == current_user.id,
            models.UserSubtopicProgress.subtopic_id == subtopic_id
        ).first()
        
        if not progress:
            return {
                "status": "pending",
                "completed": False
            }
        
        return {
            "status": progress.status,
            "completed": progress.is_completed,
            "score": progress.score,
            "attempts": progress.attempts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/subtopic/{subtopic_id}/progress")
def save_subtopic_progress(
    subtopic_id: int,
    progress_update: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Save/update subtopic progress for current user"""
    try:
        # Validate status
        valid_statuses = ['pending', 'done', 'in-progress', 'skip']
        if progress_update.status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        # Check if progress record exists
        progress = db.query(models.UserSubtopicProgress).filter(
            models.UserSubtopicProgress.user_id == current_user.id,
            models.UserSubtopicProgress.subtopic_id == subtopic_id
        ).first()
        
        if not progress:
            # Create new progress record
            progress = models.UserSubtopicProgress(
                user_id=current_user.id,
                subtopic_id=subtopic_id,
                status=progress_update.status,
                is_completed=(progress_update.status == 'done')
            )
            db.add(progress)
        else:
            # Update existing progress record
            progress.status = progress_update.status
            progress.is_completed = (progress_update.status == 'done')
        
        db.commit()
        db.refresh(progress)
        
        return {
            "success": True,
            "status": progress.status,
            "completed": progress.is_completed
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.delete("/subtopic/{subtopic_id}/progress")
def reset_subtopic_progress(
    subtopic_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Reset subtopic progress for current user (set to pending)"""
    try:
        # Find progress record
        progress = db.query(models.UserSubtopicProgress).filter(
            models.UserSubtopicProgress.user_id == current_user.id,
            models.UserSubtopicProgress.subtopic_id == subtopic_id
        ).first()
        
        if not progress:
            raise HTTPException(status_code=404, detail="Progress record not found")
        
        # Reset to pending status
        progress.status = 'pending'
        progress.is_completed = False
        progress.score = 0
        progress.accuracy = 0
        progress.attempts = 0
        
        db.commit()
        db.refresh(progress)
        
        return {
            "success": True,
            "status": progress.status,
            "message": "Progress reset to pending"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")