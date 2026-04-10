from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ..database import get_db
from ..dependencies import get_current_user
from ..services.explanation_generator import (
    generate_and_store_explanations
)
from ..services.ai_services import (
    generate_mcq_questions, 
    simplify_explanation, 
    expand_explanation,
    tutor_answer_question,
    generate_question_hint,
    generate_dynamic_description
)
from .. import crud, models

router = APIRouter(prefix="/ai", tags=["AI"])


# --------------------------------------------------
# REQUEST/RESPONSE SCHEMAS
# --------------------------------------------------

class GenerateQuestionsRequest(BaseModel):
    """Request model for question generation"""
    num_questions: Optional[int] = 10
    difficulty: Optional[str] = "medium"


class TutorQuestionRequest(BaseModel):
    """Request model for asking tutor a question"""
    question: str
    subtopic_id: int


class HintRequest(BaseModel):
    """Request model for getting hints on a question"""
    question_id: int
    hint_level: Optional[int] = 1  # 1=general, 2=step-by-step, 3=answer


# --------------------------------------------------
# ENDPOINTS
# --------------------------------------------------

@router.post("/generate-all-explanations")
def generate_all_explanations(
    db: Session = Depends(get_db)
):
    """
    Generate AI explanations for all subtopics without explanations.
    This is a bulk operation for initialization.
    """
    return generate_and_store_explanations(db)


@router.post("/generate-questions/{subtopic_id}")
def generate_questions_endpoint(
    subtopic_id: int,
    request: GenerateQuestionsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate MCQ questions for a specific subtopic using Ollama.
    
    - Validates num_questions (5, 10, or 20)
    - Validates difficulty (easy, medium, hard)
    - Generates questions via Ollama
    - Saves to database avoiding duplicates
    - Returns statistics
    
    Args:
        subtopic_id: ID of the subtopic
        request: GenerateQuestionsRequest with num_questions and difficulty
    
    Returns:
        {
            "success": bool,
            "subtopic_id": int,
            "saved": int,
            "total_now": int,
            "message": str,
            "error": str (if failed)
        }
    """
    
    # Validate num_questions
    if request.num_questions not in [5, 10, 20]:
        raise HTTPException(
            status_code=400,
            detail="num_questions must be 5, 10, or 20"
        )
    
    # Validate difficulty
    if request.difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(
            status_code=400,
            detail="difficulty must be easy, medium, or hard"
        )
    
    # Get subtopic
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == subtopic_id
    ).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=404,
            detail=f"Subtopic {subtopic_id} not found"
        )
    
    # Get topic_id from subtopic relationship
    topic_id = subtopic.topic_id
    
    try:
        # Generate questions using Ollama
        result = generate_mcq_questions(
            subtopic_title=subtopic.title,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )
        
        # Check if generation was successful
        if not result.get("success"):
            return {
                "success": False,
                "subtopic_id": subtopic_id,
                "error": result.get("error", "Unknown error during generation"),
                "message": "Failed to generate questions"
            }
        
        # Get generated questions
        questions = result.get("questions", [])
        
        if not questions:
            return {
                "success": False,
                "subtopic_id": subtopic_id,
                "error": "No valid questions were generated",
                "message": "Generation failed - empty result"
            }
        
        # Save questions to database
        save_result = crud.save_generated_questions(
            db=db,
            subtopic_id=subtopic_id,
            topic_id=topic_id,
            questions_list=questions
        )
        
        return {
            "success": True,
            "subtopic_id": subtopic_id,
            "subtopic_title": subtopic.title,
            "saved": save_result["saved"],
            "skipped": save_result["skipped"],
            "total_now": save_result["total_now"],
            "message": save_result["message"],
            "difficulty": request.difficulty
        }
        
    except Exception as e:
        return {
            "success": False,
            "subtopic_id": subtopic_id,
            "error": str(e),
            "message": "Unexpected error during question generation"
        }


@router.get("/questions/status/{subtopic_id}")
def get_questions_status(
    subtopic_id: int,
    db: Session = Depends(get_db)
):
    """
    Check the number of questions available for a subtopic.
    
    Args:
        subtopic_id: ID of the subtopic
    
    Returns:
        {
            "subtopic_id": int,
            "total_questions": int,
            "by_difficulty": {
                "easy": int,
                "medium": int,
                "hard": int
            },
            "has_sufficient_questions": bool
        }
    """
    
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == subtopic_id
    ).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=404,
            detail=f"Subtopic {subtopic_id} not found"
        )
    
    # Get total questions
    total = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id
    ).count()
    
    # Get questions by difficulty
    easy = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id,
        models.Question.difficulty == "easy"
    ).count()
    
    medium = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id,
        models.Question.difficulty == "medium"
    ).count()
    
    hard = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id,
        models.Question.difficulty == "hard"
    ).count()
    
    return {
        "subtopic_id": subtopic_id,
        "subtopic_title": subtopic.title,
        "total_questions": total,
        "by_difficulty": {
            "easy": easy,
            "medium": medium,
            "hard": hard
        },
        "has_sufficient_questions": total >= 10
    }


# --------------------------------------------------
# ADAPTIVE EXPLANATION ENDPOINT (TASK 1)
# --------------------------------------------------

@router.get("/explanation/{subtopic_id}")
def get_adaptive_explanation(
    subtopic_id: int,
    topic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get adaptive explanation based on user's learning level.
    
    - Beginner (accuracy < 40%): SIMPLE explanation (2-3 sentences)
    - Intermediate (accuracy 40-70%): STANDARD explanation (stored)
    - Advanced (accuracy > 70%): ADVANCED explanation (expanded)
    - New user: STANDARD explanation (default)
    
    Args:
        subtopic_id: ID of the subtopic
        topic_id: ID of the topic (for accuracy lookup)
        
    Returns:
        {
            "subtopic_id": int,
            "explanation": str,
            "level": str (simple/standard/advanced),
            "user_accuracy": float or None
        }
    """
    
    # Get subtopic
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == subtopic_id
    ).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=404,
            detail=f"Subtopic {subtopic_id} not found"
        )
    
    # Get user's accuracy for this topic
    accuracy_data = crud.get_user_topic_accuracy(
        db=db,
        user_id=current_user.id,
        topic_id=topic_id
    )
    
    # Determine explanation level and get explanation
    if accuracy_data is None:
        # NEW USER - show standard explanation
        level = "standard"
        explanation = subtopic.description
    else:
        accuracy = accuracy_data["accuracy"]
        
        if accuracy < 40:
            # BEGINNER - simplify explanation
            level = "simple"
            explanation = simplify_explanation(subtopic.description)
        elif accuracy < 70:
            # INTERMEDIATE - show standard explanation
            level = "standard"
            explanation = subtopic.description
        else:
            # ADVANCED - expand explanation
            level = "advanced"
            explanation = expand_explanation(subtopic.description)
    
    return {
        "subtopic_id": subtopic_id,
        "subtopic_title": subtopic.title,
        "explanation": explanation,
        "explanation_level": level,
        "user_accuracy": accuracy_data["accuracy"] if accuracy_data else None,
        "message": f"Explanation adapted for {level} learner"
    }


# --------------------------------------------------
# AI TUTORING SYSTEM ENDPOINTS (TASK 3)
# --------------------------------------------------

@router.post("/ask-tutor")
def ask_tutor(
    request: TutorQuestionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Ask the AI tutor a question about a specific subtopic.
    
    The tutor will provide a personalized answer explaining the concept.
    
    Request:
    {
        "question": "What is the difference between mean and median?",
        "subtopic_id": 42
    }
    
    Returns:
        {
            "topic": str,
            "question": str,
            "answer": str,
            "message": str
        }
    """
    
    # Get subtopic
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == request.subtopic_id
    ).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=404,
            detail=f"Subtopic {request.subtopic_id} not found"
        )
    
    try:
        # Get AI tutor answer
        answer = tutor_answer_question(
            subtopic_title=subtopic.title,
            user_question=request.question
        )
        
        return {
            "subtopic_id": request.subtopic_id,
            "subtopic_title": subtopic.title,
            "question": request.question,
            "answer": answer,
            "message": "Tutor answered your question successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating tutoring response: {str(e)}"
        )


@router.post("/hint")
def get_question_hint(
    request: HintRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get progressive hints for a question to help struggling students.
    
    Hint Levels:
    - Level 1: General guidance (don't reveal answer)
    - Level 2: Step-by-step approach (help eliminate options)
    - Level 3: Direct answer with explanation
    
    Request:
    {
        "question_id": 485,
        "hint_level": 1
    }
    
    Returns:
        {
            "question_id": int,
            "hint_level": int,
            "hint": str,
            "message": str
        }
    """
    
    # Validate hint level
    if request.hint_level not in [1, 2, 3]:
        raise HTTPException(
            status_code=400,
            detail="hint_level must be 1, 2, or 3"
        )
    
    # Get question
    question = db.query(models.Question).filter(
        models.Question.id == request.question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"Question {request.question_id} not found"
        )
    
    try:
        # Generate hint
        hint = generate_question_hint(
            question=question.question,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
            hint_level=request.hint_level
        )
        
        hint_level_names = {1: "General", 2: "Step-by-Step", 3: "Answer"}
        
        return {
            "question_id": request.question_id,
            "question": question.question,
            "hint_level": request.hint_level,
            "hint_type": hint_level_names[request.hint_level],
            "hint": hint,
            "message": f"{hint_level_names[request.hint_level]} hint provided"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating hint: {str(e)}"
        )


# --------------------------------------------------
# DYNAMIC DESCRIPTION GENERATOR (For Subtopic Panel)
# --------------------------------------------------

class DynamicDescriptionRequest(BaseModel):
    """Request model for generating dynamic descriptions"""
    title: str


@router.post("/generate-description")
def generate_subtopic_description(
    request: DynamicDescriptionRequest,
    current_user = Depends(get_current_user)
):
    """
    Generate a dynamic, on-the-fly description for a subtopic.
    
    NOT stored in database - generated in real-time using Ollama.
    Perfect for displaying in the subtopic side panel.
    
    Request:
    {
        "title": "Kinematics"
    }
    
    Response:
    {
        "title": "Kinematics",
        "description": "**Definition:**\nKinematics is the study of motion...",
        "generated_at": "2026-04-10T10:30:00",
        "success": true
    }
    """
    
    if not request.title or len(request.title.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    
    try:
        # Generate description dynamically
        description = generate_dynamic_description(request.title)
        
        return {
            "title": request.title,
            "description": description,
            "generated_at": str(__import__('datetime').datetime.utcnow()),
            "success": True,
            "message": "Description generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating description: {str(e)}"
        )


@router.get("/generate-description/{subtopic_id}")
def get_subtopic_description(
    subtopic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get dynamic description for a specific subtopic by ID.
    
    Fetches the subtopic from database and generates description on-the-fly.
    """
    
    # Get subtopic from database
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == subtopic_id
    ).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=404,
            detail=f"Subtopic {subtopic_id} not found"
        )
    
    try:
        # Generate description dynamically
        description = generate_dynamic_description(subtopic.title)
        
        return {
            "subtopic_id": subtopic_id,
            "title": subtopic.title,
            "description": description,
            "generated_at": str(__import__('datetime').datetime.utcnow()),
            "success": True,
            "message": "Description generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating description: {str(e)}"
        )