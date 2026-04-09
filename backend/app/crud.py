from sqlalchemy.orm import Session
from app import models
from app.auth import hash_password
from sqlalchemy.sql import text
import random
from datetime import datetime


# --------------------------------------------------
# 🔐 USER FUNCTIONS
# --------------------------------------------------

def create_user(db: Session, user):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# --------------------------------------------------
# 📚 CONTENT FUNCTIONS
# --------------------------------------------------

def get_subtopics_by_topic(db: Session, topic_id: int):
    return db.query(models.Subtopic).filter(models.Subtopic.topic_id == topic_id).all()


# --------------------------------------------------
# 🧠 TOPIC COMPLETION LOGIC
# --------------------------------------------------

def check_topic_completion(db: Session, user_id: int, topic_id: int):
    total = db.execute(
        """
        SELECT COUNT(*) FROM subtopics WHERE topic_id = :topic_id
        """,
        {"topic_id": topic_id}
    ).scalar()

    completed = db.execute(
        """
        SELECT COUNT(*) FROM user_subtopic_progress usp
        JOIN subtopics s ON usp.subtopic_id = s.id
        WHERE usp.user_id = :user_id
        AND s.topic_id = :topic_id
        AND usp.is_completed = TRUE
        """,
        {"user_id": user_id, "topic_id": topic_id}
    ).scalar()

    return total == completed


def update_topic_progress(db: Session, user_id: int, topic_id: int):
    is_complete = check_topic_completion(db, user_id, topic_id)

    progress = db.query(models.UserTopicProgress).filter(
        models.UserTopicProgress.user_id == user_id,
        models.UserTopicProgress.topic_id == topic_id
    ).first()

    if progress:
        progress.is_completed = is_complete
    else:
        progress = models.UserTopicProgress(
            user_id=user_id,
            topic_id=topic_id,
            is_completed=is_complete
        )
        db.add(progress)

    db.commit()


# --------------------------------------------------
# 📊 SUBTOPIC PROGRESS
# --------------------------------------------------

def update_subtopic_progress(db: Session, user_id: int, data):
    progress = db.query(models.UserSubtopicProgress).filter(
        models.UserSubtopicProgress.user_id == user_id,
        models.UserSubtopicProgress.subtopic_id == data.subtopic_id
    ).first()

    if progress:
        progress.score = data.score
        progress.accuracy = data.accuracy
        progress.time_spent = data.time_spent
        progress.attempts += 1
        progress.is_completed = True
    else:
        progress = models.UserSubtopicProgress(
            user_id=user_id,
            subtopic_id=data.subtopic_id,
            score=data.score,
            accuracy=data.accuracy,
            time_spent=data.time_spent,
            is_completed=True
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)

    # 🔥 IMPORTANT: update topic completion
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == data.subtopic_id
    ).first()

    if subtopic:
        update_topic_progress(db, user_id, subtopic.topic_id)

    return progress


# --------------------------------------------------
# 📝 TOPIC TEST (MOCK / ADAPTIVE)
# --------------------------------------------------

def create_topic_test(db: Session, user_id: int, topic_id: int, data):
    test = models.TopicTest(
        user_id=user_id,
        topic_id=topic_id,
        score=data.score,
        accuracy=data.accuracy,
        total_questions=data.total_questions,
        correct_answers=data.correct_answers,
        time_taken=data.time_taken
    )

    db.add(test)

    # ✅ PASS CONDITION (can adjust later)
    if data.accuracy >= 60:
        progress = db.query(models.UserTopicProgress).filter(
            models.UserTopicProgress.user_id == user_id,
            models.UserTopicProgress.topic_id == topic_id
        ).first()

        if progress:
            progress.is_completed = True

    db.commit()
    db.refresh(test)

    return test

def get_weak_subtopics(db: Session, user_id: int):
    weak = db.query(models.UserSubtopicProgress).filter(
        models.UserSubtopicProgress.user_id == user_id,
        models.UserSubtopicProgress.accuracy < 60
    ).all()

    return weak

def get_adaptive_questions(db, user_id: int, topic_id: int, num_questions: int = 10):
    """
    Get adaptive questions for testing with focus on weak areas.
    - If weak subtopic found: Get 5-6 from weak area + fill rest from other subtopics
    - If no weak area: Get diverse questions from topic
    """

    # 1️⃣ Get topic progress to determine difficulty
    progress = db.query(models.UserTopicProgress).filter(
        models.UserTopicProgress.user_id == user_id,
        models.UserTopicProgress.topic_id == topic_id
    ).first()

    difficulty = "easy"

    if progress and progress.accuracy is not None:
        if progress.accuracy < 40:
            difficulty = "easy"
        elif progress.accuracy < 70:
            difficulty = "medium"
        else:
            difficulty = "hard"

    # 2️⃣ Get weak subtopic
    weak_subtopic_id = get_weak_subtopic(db, user_id, topic_id)

    questions = []

    # 3️⃣ If weak exists → focus on it first
    if weak_subtopic_id:
        print(f"Weak Subtopic found: {weak_subtopic_id}")
        
        # Get 5-6 questions from weak subtopic
        weak_questions = db.query(models.Question).filter(
            models.Question.topic_id == topic_id,
            models.Question.subtopic_id == weak_subtopic_id,
            models.Question.difficulty == difficulty
        ).limit(6).all()
        
        questions.extend(weak_questions)
        
        # Fill remaining slots from other subtopics
        remaining = num_questions - len(questions)
        if remaining > 0:
            other_questions = db.query(models.Question).filter(
                models.Question.topic_id == topic_id,
                models.Question.subtopic_id != weak_subtopic_id,
                models.Question.difficulty == difficulty
            ).limit(remaining).all()
            questions.extend(other_questions)
    else:
        print("No weak subtopic — getting diverse questions")
        
        # Get from all subtopics
        questions = db.query(models.Question).filter(
            models.Question.topic_id == topic_id,
            models.Question.difficulty == difficulty
        ).limit(num_questions).all()

    print(f"Difficulty: {difficulty}")
    print(f"Questions found: {len(questions)}")

    return questions

def get_weak_subtopic(db, user_id: int, topic_id: int):

    weak = db.query(models.UserSubtopicProgress).join(
        models.Subtopic,
        models.Subtopic.id == models.UserSubtopicProgress.subtopic_id
    ).filter(
        models.UserSubtopicProgress.user_id == user_id,
        models.Subtopic.topic_id == topic_id,
        models.UserSubtopicProgress.accuracy < 60
    ).order_by(
        models.UserSubtopicProgress.accuracy.asc()
    ).first()

    if weak:
        return weak.subtopic_id

    return None


# --------------------------------------------------
# 🤖 AI QUESTION GENERATION & STORAGE
# --------------------------------------------------

def save_generated_questions(db: Session, subtopic_id: int, topic_id: int, questions_list: list):
    """
    Save generated questions to the database.
    
    Args:
        db: Database session
        subtopic_id: ID of the subtopic
        topic_id: ID of the topic
        questions_list: List of question dictionaries from AI
    
    Returns:
        Dict with save statistics
    """
    
    # Check existing questions count
    existing_count = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id
    ).count()
    
    # Target: at least 10 questions per subtopic
    target_count = 10
    needed = max(0, target_count - existing_count)
    
    saved_count = 0
    skipped_count = 0
    
    # Save only needed questions
    for question_data in questions_list[:needed]:
        try:
            # Check for duplicates
            existing = db.query(models.Question).filter(
                models.Question.subtopic_id == subtopic_id,
                models.Question.question == question_data.get("question")
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Create new question record
            question = models.Question(
                topic_id=topic_id,
                subtopic_id=subtopic_id,
                difficulty=question_data.get("difficulty", "medium"),
                question=question_data.get("question"),
                option_a=question_data.get("option_a"),
                option_b=question_data.get("option_b"),
                option_c=question_data.get("option_c"),
                option_d=question_data.get("option_d"),
                correct_answer=question_data.get("correct_answer")
            )
            
            db.add(question)
            saved_count += 1
            
        except Exception as e:
            print(f"Error saving question: {str(e)}")
            skipped_count += 1
            continue
    
    # Commit all changes
    db.commit()
    
    # Get final count
    final_count = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id
    ).count()
    
    return {
        "subtopic_id": subtopic_id,
        "saved": saved_count,
        "skipped": skipped_count,
        "total_now": final_count,
        "message": f"Saved {saved_count} questions. Total for subtopic: {final_count}"
    }


def get_questions_by_subtopic(db: Session, subtopic_id: int, difficulty: str = None):
    """
    Get questions for a subtopic, optionally filtered by difficulty.
    
    Args:
        db: Database session
        subtopic_id: ID of the subtopic
        difficulty: Optional filter (easy/medium/hard)
    
    Returns:
        List of questions
    """
    
    query = db.query(models.Question).filter(
        models.Question.subtopic_id == subtopic_id
    )
    
    if difficulty:
        query = query.filter(models.Question.difficulty == difficulty)
    
    return query.all()


# --------------------------------------------------
# 📊 GET USER ACCURACY (for adaptive explanations)
# --------------------------------------------------

def get_user_topic_accuracy(db: Session, user_id: int, topic_id: int):
    """
    Get user's accuracy for a specific topic.
    
    Args:
        db: Database session
        user_id: User ID
        topic_id: Topic ID
    
    Returns:
        Dict with accuracy information or None if no progress
    """
    
    progress = db.query(models.UserTopicProgress).filter(
        models.UserTopicProgress.user_id == user_id,
        models.UserTopicProgress.topic_id == topic_id
    ).first()
    
    if progress is None or progress.accuracy is None:
        return None  # No progress data yet
    
    return {
        "accuracy": progress.accuracy,
        "is_completed": progress.is_completed,
        "last_score": progress.last_score
    }


# --------------------------------------------------
# 💬 CHAT SESSION AND MESSAGE MANAGEMENT
# --------------------------------------------------

def create_chat_session(
    db: Session,
    user_id: int,
    topic_id: int = None,
    subtopic_id: int = None,
    title: str = None
):
    """
    Create a new chat session for a user.
    """
    
    session = models.ChatSession(
        user_id=user_id,
        topic_id=topic_id,
        subtopic_id=subtopic_id,
        title=title or "Chat Session"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session


def add_chat_message(
    db: Session,
    session_id: int,
    role: str,  # "user" or "assistant"
    content: str
):
    """
    Add a message to chat session.
    """
    
    message = models.ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


def get_chat_history(db: Session, session_id: int):
    """
    Get all messages in a chat session.
    """
    
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.session_id == session_id
    ).order_by(models.ChatMessage.created_at.asc()).all()
    
    return [
        {
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at
        }
        for msg in messages
    ]


def get_chat_session(db: Session, session_id: int, user_id: int):
    """
    Get a chat session (verify ownership).
    """
    
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == user_id
    ).first()
    
    return session


def get_user_chat_sessions(db: Session, user_id: int):
    """
    Get all chat sessions for a user.
    """
    
    sessions = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user_id
    ).order_by(models.ChatSession.updated_at.desc()).all()
    
    return sessions


def end_chat_session(db: Session, session_id: int):
    """
    Delete a chat session and all its messages.
    """
    
    try:
        # Delete all messages in the session first
        db.query(models.ChatMessage).filter(
            models.ChatMessage.session_id == session_id
        ).delete()
        
        # Delete the session
        session = db.query(models.ChatSession).filter(
            models.ChatSession.id == session_id
        ).first()
        
        if session:
            db.delete(session)
            db.commit()
            return {"deleted": True}
        
        return {"deleted": False}
    except Exception as e:
        db.rollback()
        raise e