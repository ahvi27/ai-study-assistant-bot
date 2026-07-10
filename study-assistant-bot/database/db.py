"""
Database module for Study Assistant Bot.
Manages database connections and session management.
"""

from typing import Optional, Type, List, Any, Generator
from sqlalchemy import create_engine, Engine, select, and_, or_
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from datetime import datetime, timedelta
from config import Config
from database.models import Base, User, Document, Question, Quiz, Flashcard, Reminder, StudyPlan, Progress, DocumentChunk
import logging

logger = logging.getLogger(__name__)

# Create engine
if "sqlite" in Config.DATABASE_URL:
    engine: Engine = create_engine(
        Config.DATABASE_URL,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine: Engine = create_engine(
        Config.DATABASE_URL,
        echo=False,
        future=True,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

# Scoped session for thread-safe operations
scoped_session_factory = scoped_session(SessionLocal)


def init_db() -> None:
    """Initialize database and create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def get_session() -> Session:
    """Get a new database session"""
    return SessionLocal()


@contextmanager
def get_db_context():
    """Context manager for database session"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()


class Database:
    """Database operations wrapper"""

    @staticmethod
    def add(session: Session, obj: Any) -> Any:
        """Add object to database"""
        try:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding object: {e}")
            raise

    @staticmethod
    def update(session: Session, obj: Any) -> Any:
        """Update object in database"""
        try:
            session.merge(obj)
            session.commit()
            return obj
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating object: {e}")
            raise

    @staticmethod
    def delete(session: Session, obj: Any) -> None:
        """Delete object from database"""
        try:
            session.delete(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting object: {e}")
            raise

    @staticmethod
    def get(session: Session, model: Type, **kwargs) -> Optional[Any]:
        """Get single object by filters"""
        try:
            query = select(model)
            for key, value in kwargs.items():
                query = query.where(getattr(model, key) == value)
            return session.scalar(query)
        except Exception as e:
            logger.error(f"Error getting object: {e}")
            return None

    @staticmethod
    def get_all(session: Session, model: Type, **kwargs) -> List[Any]:
        """Get all objects matching filters"""
        try:
            query = select(model)
            for key, value in kwargs.items():
                query = query.where(getattr(model, key) == value)
            return session.scalars(query).all()
        except Exception as e:
            logger.error(f"Error getting objects: {e}")
            return []

    @staticmethod
    def get_paginated(session: Session, model: Type, page: int = 1, page_size: int = 10, **kwargs) -> tuple[List[Any], int]:
        """Get paginated objects"""
        try:
            query = select(model)
            for key, value in kwargs.items():
                query = query.where(getattr(model, key) == value)

            total = session.scalar(select(model).where(
                and_(*(getattr(model, k) == v for k, v in kwargs.items()))
            ) if kwargs else select(model))

            offset = (page - 1) * page_size
            query = query.limit(page_size).offset(offset)
            results = session.scalars(query).all()

            return results, len(results)
        except Exception as e:
            logger.error(f"Error getting paginated objects: {e}")
            return [], 0


# User operations
class UserDB:
    """User database operations"""

    @staticmethod
    def create_user(session: Session, telegram_id: int, username: str = None, first_name: str = None, last_name: str = None) -> User:
        """Create new user"""
        existing_user = Database.get(session, User, telegram_id=telegram_id)
        if existing_user:
            return existing_user

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        return Database.add(session, user)

    @staticmethod
    def get_user(session: Session, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        return Database.get(session, User, telegram_id=telegram_id)

    @staticmethod
    def update_user_activity(session: Session, telegram_id: int) -> Optional[User]:
        """Update user's last activity timestamp"""
        from datetime import datetime
        user = UserDB.get_user(session, telegram_id)
        if user:
            user.last_activity = datetime.utcnow()
            return Database.update(session, user)
        return None

    @staticmethod
    def update_study_stats(session: Session, telegram_id: int, minutes: int = 0, documents: int = 0, questions: int = 0, quizzes: int = 0) -> Optional[User]:
        """Update user study statistics"""
        user = UserDB.get_user(session, telegram_id)
        if user:
            if minutes:
                user.total_study_time += minutes
            if documents:
                user.total_documents += documents
            if questions:
                user.total_questions += questions
            if quizzes:
                user.total_quizzes += quizzes
            return Database.update(session, user)
        return None


# Document operations
class DocumentDB:
    """Document database operations"""

    @staticmethod
    def add_document(session: Session, user_id: int, filename: str, file_path: str, file_type: str, file_size: int, original_filename: str = None) -> Document:
        """Add new document"""
        doc = Document(
            user_id=user_id,
            filename=filename,
            original_filename=original_filename or filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
        )
        return Database.add(session, doc)

    @staticmethod
    def get_user_documents(session: Session, user_id: int) -> List[Document]:
        """Get all documents for user"""
        return Database.get_all(session, Document, user_id=user_id)

    @staticmethod
    def get_document(session: Session, document_id: int) -> Optional[Document]:
        """Get document by ID"""
        return Database.get(session, Document, id=document_id)

    @staticmethod
    def update_document_content(session: Session, document_id: int, text_content: str, page_count: int = 1) -> Optional[Document]:
        """Update document with extracted content"""
        doc = DocumentDB.get_document(session, document_id)
        if doc:
            doc.text_content = text_content
            doc.page_count = page_count
            doc.is_processed = True
            return Database.update(session, doc)
        return None


# Question operations
class QuestionDB:
    """Question database operations"""

    @staticmethod
    def add_question(session: Session, user_id: int, question_text: str, answer_text: str = None, document_id: int = None, source: str = "ai") -> Question:
        """Add new question"""
        question = Question(
            user_id=user_id,
            question_text=question_text,
            answer_text=answer_text,
            document_id=document_id,
            source=source,
        )
        return Database.add(session, question)

    @staticmethod
    def get_user_questions(session: Session, user_id: int, limit: int = 10) -> List[Question]:
        """Get user's recent questions"""
        query = select(Question).where(Question.user_id == user_id).order_by(Question.created_at.desc()).limit(limit)
        return session.scalars(query).all()


# Quiz operations
class QuizDB:
    """Quiz database operations"""

    @staticmethod
    def create_quiz(session: Session, user_id: int, quiz_data: dict, difficulty: str, total_questions: int, document_id: int = None) -> Quiz:
        """Create new quiz"""
        quiz = Quiz(
            user_id=user_id,
            quiz_data=quiz_data,
            difficulty=difficulty,
            total_questions=total_questions,
            document_id=document_id,
        )
        return Database.add(session, quiz)

    @staticmethod
    def complete_quiz(session: Session, quiz_id: int, correct_answers: int, time_taken: int) -> Optional[Quiz]:
        """Mark quiz as completed and save score"""
        from datetime import datetime
        quiz = Database.get(session, Quiz, id=quiz_id)
        if quiz:
            quiz.correct_answers = correct_answers
            quiz.score = (correct_answers / quiz.total_questions) * 100
            quiz.time_taken = time_taken
            quiz.completed = True
            quiz.completed_at = datetime.utcnow()
            return Database.update(session, quiz)
        return None

    @staticmethod
    def get_user_quizzes(session: Session, user_id: int, limit: int = 10) -> List[Quiz]:
        """Get user's quizzes"""
        query = select(Quiz).where(Quiz.user_id == user_id).order_by(Quiz.created_at.desc()).limit(limit)
        return session.scalars(query).all()


# Flashcard operations
class FlashcardDB:
    """Flashcard database operations"""

    @staticmethod
    def create_flashcard(session: Session, user_id: int, question: str, answer: str, difficulty: str = "medium", document_id: int = None) -> Flashcard:
        """Create new flashcard"""
        flashcard = Flashcard(
            user_id=user_id,
            question=question,
            answer=answer,
            difficulty=difficulty,
            document_id=document_id,
        )
        return Database.add(session, flashcard)

    @staticmethod
    def get_user_flashcards(session: Session, user_id: int) -> List[Flashcard]:
        """Get user's flashcards"""
        return Database.get_all(session, Flashcard, user_id=user_id)

    @staticmethod
    def get_pending_review(session: Session, user_id: int, limit: int = 5) -> List[Flashcard]:
        """Get flashcards pending review"""
        from datetime import datetime
        query = select(Flashcard).where(
            and_(
                Flashcard.user_id == user_id,
                or_(
                    Flashcard.next_review.is_(None),
                    Flashcard.next_review <= datetime.utcnow()
                )
            )
        ).limit(limit)
        return session.scalars(query).all()

    @staticmethod
    def mark_flashcard_reviewed(session: Session, flashcard_id: int, correct: bool) -> Optional[Flashcard]:
        """Mark flashcard as reviewed"""
        from datetime import datetime, timedelta
        flashcard = Database.get(session, Flashcard, id=flashcard_id)
        if flashcard:
            flashcard.times_reviewed += 1
            if correct:
                flashcard.times_correct += 1
            flashcard.last_reviewed = datetime.utcnow()
            # Simple spaced repetition: next review in 1, 3, 7 days based on correct count
            review_intervals = {1: 1, 2: 3, 3: 7}
            interval = review_intervals.get(flashcard.times_correct, 14)
            flashcard.next_review = datetime.utcnow() + timedelta(days=interval)
            return Database.update(session, flashcard)
        return None


# Reminder operations
class ReminderDB:
    """Reminder database operations"""

    @staticmethod
    def create_reminder(session: Session, user_id: int, message: str, scheduled_time, reminder_type: str = "custom", recurrence: str = None) -> Reminder:
        """Create new reminder"""
        reminder = Reminder(
            user_id=user_id,
            message=message,
            scheduled_time=scheduled_time,
            reminder_type=reminder_type,
            recurrence=recurrence,
        )
        return Database.add(session, reminder)

    @staticmethod
    def get_user_reminders(session: Session, user_id: int) -> List[Reminder]:
        """Get user's active reminders"""
        return Database.get_all(session, Reminder, user_id=user_id, is_active=True)

    @staticmethod
    def get_pending_reminders(session: Session) -> List[Reminder]:
        """Get all reminders that should be sent now"""
        from datetime import datetime
        query = select(Reminder).where(
            and_(
                Reminder.is_active == True,
                Reminder.scheduled_time <= datetime.utcnow()
            )
        )
        return session.scalars(query).all()


# StudyPlan operations
class StudyPlanDB:
    """Study plan database operations"""

    @staticmethod
    def create_study_plan(session: Session, user_id: int, title: str, subjects: list, exam_date, daily_hours: float, plan_data: dict, description: str = None) -> StudyPlan:
        """Create new study plan"""
        plan = StudyPlan(
            user_id=user_id,
            title=title,
            subjects=subjects,
            exam_date=exam_date,
            daily_study_hours=daily_hours,
            plan_data=plan_data,
            description=description,
        )
        return Database.add(session, plan)

    @staticmethod
    def get_user_plans(session: Session, user_id: int) -> List[StudyPlan]:
        """Get user's study plans"""
        return Database.get_all(session, StudyPlan, user_id=user_id, is_active=True)


# Progress operations
class ProgressDB:
    """Progress database operations"""

    @staticmethod
    def get_or_create_progress(session: Session, user_id: int) -> Progress:
        """Get or create user progress record"""
        progress = Database.get(session, Progress, user_id=user_id)
        if not progress:
            progress = Progress(user_id=user_id)
            return Database.add(session, progress)
        return progress

    @staticmethod
    def update_progress(session: Session, user_id: int, **kwargs) -> Optional[Progress]:
        """Update user progress"""
        progress = ProgressDB.get_or_create_progress(session, user_id)
        if progress:
            for key, value in kwargs.items():
                if hasattr(progress, key):
                    setattr(progress, key, value)
            return Database.update(session, progress)
        return None
