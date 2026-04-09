from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.services.ai_services import generate_chat_response
from app import crud, models

router = APIRouter(prefix="/chat", tags=["Chat"])


# --------------------------------------------------
# REQUEST/RESPONSE SCHEMAS
# --------------------------------------------------

class StartChatRequest(BaseModel):
    """Request to start a new chat session"""
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    title: Optional[str] = None


class SendMessageRequest(BaseModel):
    """Request to send a message in chat"""
    session_id: int
    message: str


class ChatMessageResponse(BaseModel):
    """Single chat message"""
    role: str
    content: str


# --------------------------------------------------
# CHAT ENDPOINTS
# --------------------------------------------------

@router.post("/start-session")
def start_chat_session(
    request: StartChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Start a new conversational chat session.
    
    Can be general or focused on a specific topic/subtopic.
    
    Request:
    {
        "topic_id": 8,
        "subtopic_id": 42,
        "title": "Understanding Mean & Median"
    }
    
    Returns:
        {
            "session_id": 1,
            "user_id": 5,
            "topic_id": 8,
            "subtopic_id": 42,
            "title": "Understanding Mean & Median",
            "created_at": "2026-04-08T10:30:00",
            "message": "Chat session started"
        }
    """
    
    # Validate topic if provided
    if request.topic_id:
        topic = db.query(models.Topic).filter(
            models.Topic.id == request.topic_id
        ).first()
        
        if not topic:
            raise HTTPException(
                status_code=404,
                detail=f"Topic {request.topic_id} not found"
            )
    
    # Validate subtopic if provided
    if request.subtopic_id:
        subtopic = db.query(models.Subtopic).filter(
            models.Subtopic.id == request.subtopic_id
        ).first()
        
        if not subtopic:
            raise HTTPException(
                status_code=404,
                detail=f"Subtopic {request.subtopic_id} not found"
            )
    
    try:
        # Create chat session
        session = crud.create_chat_session(
            db=db,
            user_id=current_user.id,
            topic_id=request.topic_id,
            subtopic_id=request.subtopic_id,
            title=request.title
        )
        
        return {
            "session_id": session.id,
            "user_id": session.user_id,
            "topic_id": session.topic_id,
            "subtopic_id": session.subtopic_id,
            "title": session.title,
            "created_at": session.created_at,
            "message": "Chat session started successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating chat session: {str(e)}"
        )


@router.post("/send-message")
def send_chat_message(
    request: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Send a message in an active chat session.
    
    The AI tutor will respond maintaining conversation context.
    
    Request:
    {
        "session_id": 1,
        "message": "What is the difference between mean and median?"
    }
    
    Returns:
        {
            "session_id": 1,
            "user_message": "What is the difference...",
            "assistant_response": "Mean is the average...",
            "message_count": 4
        }
    """
    
    # Verify session belongs to user
    chat_session = crud.get_chat_session(
        db=db,
        session_id=request.session_id,
        user_id=current_user.id
    )
    
    if not chat_session:
        raise HTTPException(
            status_code=404,
            detail=f"Chat session {request.session_id} not found or unauthorized"
        )
    
    try:
        # Get conversation history
        history = crud.get_chat_history(db=db, session_id=request.session_id)
        
        # Get context information
        topic_title = None
        subtopic_title = None
        
        if chat_session.subtopic_id:
            subtopic = db.query(models.Subtopic).filter(
                models.Subtopic.id == chat_session.subtopic_id
            ).first()
            if subtopic:
                subtopic_title = subtopic.title
        
        if chat_session.topic_id:
            topic = db.query(models.Topic).filter(
                models.Topic.id == chat_session.topic_id
            ).first()
            if topic:
                topic_title = topic.title
        
        # Generate AI response
        ai_response = generate_chat_response(
            user_message=request.message,
            conversation_history=history,
            topic_context=topic_title,
            subtopic_context=subtopic_title
        )
        
        # Save user message
        crud.add_chat_message(
            db=db,
            session_id=request.session_id,
            role="user",
            content=request.message
        )
        
        # Save assistant response
        crud.add_chat_message(
            db=db,
            session_id=request.session_id,
            role="assistant",
            content=ai_response
        )
        
        # Get updated message count
        updated_history = crud.get_chat_history(db=db, session_id=request.session_id)
        
        return {
            "session_id": request.session_id,
            "user_message": request.message,
            "assistant_response": ai_response,
            "message_count": len(updated_history),
            "message": "Message sent and response generated"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending message: {str(e)}"
        )


@router.get("/history/{session_id}")
def get_session_history(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get full conversation history for a chat session.
    
    Returns all messages in chronological order.
    
    Response:
    {
        "session_id": 1,
        "topic": "Mean, Median, Mode",
        "message_count": 10,
        "messages": [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."},
            ...
        ]
    }
    """
    
    # Verify session belongs to user
    chat_session = crud.get_chat_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )
    
    if not chat_session:
        raise HTTPException(
            status_code=404,
            detail=f"Chat session {session_id} not found or unauthorized"
        )
    
    try:
        history = crud.get_chat_history(db=db, session_id=session_id)
        
        return {
            "session_id": session_id,
            "title": chat_session.title,
            "topic_id": chat_session.topic_id,
            "subtopic_id": chat_session.subtopic_id,
            "message_count": len(history),
            "messages": history,
            "created_at": chat_session.created_at,
            "updated_at": chat_session.updated_at
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )


@router.get("/sessions")
def get_user_sessions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all chat sessions for the current user.
    
    Returns list of sessions with latest message info.
    
    Response:
    {
        "total_sessions": 5,
        "sessions": [
            {
                "session_id": 1,
                "title": "Mean & Median Discussion",
                "message_count": 12,
                "created_at": "2026-04-08T10:30:00",
                "updated_at": "2026-04-08T11:45:00"
            },
            ...
        ]
    }
    """
    
    try:
        sessions = crud.get_user_chat_sessions(db=db, user_id=current_user.id)
        
        session_list = []
        for session in sessions:
            message_count = db.query(models.ChatMessage).filter(
                models.ChatMessage.session_id == session.id
            ).count()
            
            session_list.append({
                "session_id": session.id,
                "title": session.title,
                "topic_id": session.topic_id,
                "subtopic_id": session.subtopic_id,
                "message_count": message_count,
                "created_at": session.created_at,
                "updated_at": session.updated_at
            })
        
        return {
            "total_sessions": len(session_list),
            "sessions": session_list
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat sessions: {str(e)}"
        )


@router.delete("/end-session/{session_id}")
def end_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    End a chat session.
    
    Session history is preserved; just marks as ended.
    """
    
    # Verify session belongs to user
    chat_session = crud.get_chat_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )
    
    if not chat_session:
        raise HTTPException(
            status_code=404,
            detail=f"Chat session {session_id} not found or unauthorized"
        )
    
    try:
        crud.end_chat_session(db=db, session_id=session_id)
        
        message_count = db.query(models.ChatMessage).filter(
            models.ChatMessage.session_id == session_id
        ).count()
        
        return {
            "session_id": session_id,
            "status": "ended",
            "message_count": message_count,
            "message": "Chat session ended"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ending chat session: {str(e)}"
        )
