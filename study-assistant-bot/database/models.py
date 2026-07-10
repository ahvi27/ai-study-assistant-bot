"""
Database models for Study Assistant Bot.
Defines all data structures for users, documents, quizzes, flashcards, etc.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
    JSON,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model for storing user information and preferences."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_premium = Column(Boolean, default=False)
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="user", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="user", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="user", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Document(Base):
    """Document model for storing uploaded study materials."""
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer)
    text_content = Column(Text, nullable=True)
    page_count = Column(Integer, default=1)
    summary = Column(Text, nullable=True)
    is_processed = Column(Boolean, default=False)
    embeddings_generated = Column(Boolean, default=False)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="document", cascade="all, delete-orphan")
    
    __table_args__ = (Index("idx_user_id_created", "user_id", "created_at"),)


class DocumentChunk(Base):
    """Document chunk model for RAG embeddings."""
    
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True)
    tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    __table_args__ = (Index("idx_document_id_chunk_index", "document_id", "chunk_index"),)


class Question(Base):
    """Question model for storing Q&A history."""
    
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    source_type = Column(String(50), default="ai")
    used_documents = Column(JSON, nullable=True)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="questions")
    document = relationship("Document", back_populates="questions")
    
    __table_args__ = (Index("idx_user_id_created", "user_id", "created_at"),)


class Quiz(Base):
    """Quiz model for storing generated quizzes."""
    
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    quiz_data = Column(JSON, nullable=False)
    difficulty = Column(String(10), default="medium")
    total_questions = Column(Integer)
    correct_answers = Column(Integer, default=0)
    score = Column(Float, nullable=True)
    time_taken = Column(Integer, default=0)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="quizzes")
    document = relationship("Document")
    
    __table_args__ = (Index("idx_user_id_created", "user_id", "created_at"),)


class Flashcard(Base):
    """Flashcard model for storing flashcards."""
    
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    difficulty_level = Column(String(10), default="medium")
    times_reviewed = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    last_reviewed = Column(DateTime, nullable=True)
    next_review = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="flashcards")
    document = relationship("Document")
    
    __table_args__ = (Index("idx_user_id_next_review", "user_id", "next_review"),)


class Reminder(Base):
    """Reminder model for storing user reminders."""
    
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(String(1024), nullable=False)
    reminder_type = Column(String(50), default="custom")
    frequency = Column(String(50), nullable=True)
    scheduled_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reminders")
    
    __table_args__ = (Index("idx_user_id_active_scheduled", "user_id", "is_active", "scheduled_time"),)


class StudyPlan(Base):
    """Study plan model for storing personalized study plans."""
    
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subjects = Column(JSON, nullable=False)
    exam_date = Column(DateTime, nullable=False)
    daily_study_hours = Column(Float, default=2.0)
    plan_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    completion_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="study_plans")


class Progress(Base):
    """Progress model for tracking user learning progress."""
    
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    total_documents = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    total_quizzes = Column(Integer, default=0)
    total_quiz_score = Column(Float, default=0.0)
    study_streak = Column(Integer, default=0)
    total_study_minutes = Column(Integer, default=0)
    flashcards_learned = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")
