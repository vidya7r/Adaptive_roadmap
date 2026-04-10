from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Text, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from sqlalchemy.sql import func


# --------------------------------------------------
# 👤 USERS
# --------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    subtopic_progress = relationship("UserSubtopicProgress", back_populates="user")
    topic_progress = relationship("UserTopicProgress", back_populates="user")


# --------------------------------------------------
#  TOPICS
# --------------------------------------------------

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer)
    title = Column(String)

    subtopics = relationship("Subtopic", back_populates="topic")
    questions = relationship("Question", back_populates="topic")


# --------------------------------------------------
# 📚 SUBTOPICS
# --------------------------------------------------

class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"))

    title = Column(String(200), nullable=False)
    description = Column(Text)

    topic = relationship("Topic", back_populates="subtopics")
    questions = relationship("Question", back_populates="subtopic")
    progress = relationship("UserSubtopicProgress", back_populates="subtopic")
    resources = relationship("Resource", back_populates="subtopic", cascade="all, delete-orphan")


# --------------------------------------------------
# 📝 QUESTIONS
# --------------------------------------------------

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    topic_id = Column(
        Integer,
        ForeignKey("topics.id", ondelete="CASCADE")
    )

    # ✅ IMPORTANT ADDITION
    subtopic_id = Column(
        Integer,
        ForeignKey("subtopics.id", ondelete="CASCADE")
    )

    difficulty = Column(String)

    question = Column(Text)

    option_a = Column(Text)
    option_b = Column(Text)
    option_c = Column(Text)
    option_d = Column(Text)

    correct_answer = Column(String)

    topic = relationship("Topic", back_populates="questions")
    subtopic = relationship("Subtopic", back_populates="questions")


# --------------------------------------------------
# 📊 USER SUBTOPIC PROGRESS
# --------------------------------------------------

class UserSubtopicProgress(Base):
    __tablename__ = "user_subtopic_progress"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    subtopic_id = Column(
        Integer,
        ForeignKey("subtopics.id", ondelete="CASCADE")
    )

    is_completed = Column(Boolean, default=False)

    # Status field: pending, done, in-progress, skip
    status = Column(String, default='pending')

    # ✅ Add safe defaults
    score = Column(Float, default=0)
    accuracy = Column(Float, default=0)

    time_spent = Column(Integer, default=0)

    # ✅ Important fix
    attempts = Column(Integer, default=0)

    # ✅ Better timestamps
    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'subtopic_id',
            name='unique_user_subtopic'
        ),
    )

    user = relationship("User", back_populates="subtopic_progress")
    subtopic = relationship("Subtopic", back_populates="progress")


# --------------------------------------------------
# 📈 USER TOPIC PROGRESS
# --------------------------------------------------

class UserTopicProgress(Base):
    __tablename__ = "user_topic_progress"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    topic_id = Column(
        Integer,
        ForeignKey("topics.id", ondelete="CASCADE")
    )

    is_completed = Column(Boolean, default=False)

    last_score = Column(Float)
    accuracy = Column(Float)

    updated_at = Column(
        TIMESTAMP,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'topic_id',
            name='unique_user_topic'
        ),
    )

    user = relationship("User", back_populates="topic_progress")


# --------------------------------------------------
# 📝 TOPIC TESTS HISTORY
# --------------------------------------------------

class TopicTest(Base):
    __tablename__ = "topic_tests"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    topic_id = Column(
        Integer,
        ForeignKey("topics.id", ondelete="CASCADE")
    )

    score = Column(Float)
    accuracy = Column(Float)

    total_questions = Column(Integer)
    correct_answers = Column(Integer)

    time_taken = Column(Integer)

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )


# --------------------------------------------------
# 💬 CHAT SESSIONS (Conversational Tutoring)
# --------------------------------------------------

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    topic_id = Column(
        Integer,
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=True  # Chat can be general or topic-specific
    )
    
    subtopic_id = Column(
        Integer,
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=True  # Chat can be about specific subtopic
    )
    
    title = Column(String(200), nullable=True)  # e.g., "Understanding Mean"
    
    created_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


# --------------------------------------------------
# 💬 CHAT MESSAGES (stores conversation history)
# --------------------------------------------------

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    
    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True
    )
    
    role = Column(String(20))  # "user" or "assistant"
    content = Column(Text)      # Message text
    
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    session = relationship("ChatSession", back_populates="messages")


# --------------------------------------------------
# 📚 RESOURCES (Study Materials)
# --------------------------------------------------

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    
    subtopic_id = Column(
        Integer,
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        index=True
    )
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Resource type: pdf, video, link, document
    resource_type = Column(String(50), nullable=False, default="link")
    
    # URL for videos, PDFs, or external links
    url = Column(Text, nullable=True)
    
    # File path if stored locally
    file_path = Column(Text, nullable=True)
    
    # For organizing resources
    category = Column(String(100), nullable=True)  # e.g., "Recommended", "Optional", "Practice"
    
    # Order of display
    order = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    subtopic = relationship("Subtopic", back_populates="resources")