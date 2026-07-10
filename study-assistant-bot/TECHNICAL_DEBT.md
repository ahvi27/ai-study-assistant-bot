# 🔧 Technical Debt & Code Quality Improvements

This document outlines code quality improvements and technical debt that should be addressed to improve maintainability, performance, and reliability.

## Code Quality Improvements

### 1. Error Handling & Logging

#### Current Issues
- [ ] Some handlers lack comprehensive error handling
- [ ] Missing try-catch blocks in critical operations
- [ ] Inconsistent logging levels

#### Improvements
```python
# ❌ Before
async def handle_upload(update, context):
    document = await upload_service.process_file(file_path)
    # What if process_file fails?

# ✅ After
async def handle_upload(update, context):
    try:
        document = await upload_service.process_file(file_path)
        await update.message.reply_text("✅ File processed")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        await update.message.reply_text("❌ File not found")
    except ValueError as e:
        logger.warning(f"Invalid file: {e}")
        await update.message.reply_text(f"❌ Invalid file: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        await update.message.reply_text("❌ An unexpected error occurred")
```

#### Priority: 🔴 HIGH
#### Effort: Medium
#### Files to Update: All handlers in `handlers/`

---

### 2. Type Hints Completion

#### Current Issues
- [ ] Some functions missing type hints
- [ ] Return types not always specified
- [ ] Generic types could be more specific

#### Improvements
```python
# ❌ Before
def get_user_stats(user_id):
    return session.query(User).filter_by(id=user_id).first()

# ✅ After
from typing import Optional
from database.models import User

def get_user_stats(user_id: int) -> Optional[User]:
    """Get user statistics by user ID."""
    return session.query(User).filter_by(id=user_id).first()
```

#### Priority: 🟡 MEDIUM
#### Effort: Low
#### Files to Update: All service files in `services/`

---

### 3. Input Validation Enhancement

#### Current Issues
- [ ] Limited input validation in handlers
- [ ] File size limits not enforced in all places
- [ ] User input could be sanitized better

#### Improvements
```python
# In utils/validators.py - Add these functions
from typing import Tuple

def validate_flashcard_input(front: str, back: str) -> Tuple[bool, str]:
    """Validate flashcard input.
    
    Args:
        front: Front side of flashcard
        back: Back side of flashcard
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not front or len(front.strip()) == 0:
        return False, "Front side cannot be empty"
    
    if len(front) > 500:
        return False, "Front side must be less than 500 characters"
    
    if not back or len(back.strip()) == 0:
        return False, "Back side cannot be empty"
    
    if len(back) > 1000:
        return False, "Back side must be less than 1000 characters"
    
    return True, ""

def validate_quiz_parameters(
    num_questions: int,
    difficulty: str,
    question_type: str
) -> Tuple[bool, str]:
    """Validate quiz generation parameters."""
    
    if not 1 <= num_questions <= 50:
        return False, "Number of questions must be between 1 and 50"
    
    if difficulty not in ["easy", "medium", "hard"]:
        return False, "Invalid difficulty level"
    
    if question_type not in ["mcq", "true_false", "short_answer"]:
        return False, "Invalid question type"
    
    return True, ""
```

#### Priority: 🟡 MEDIUM
#### Effort: Low-Medium
#### Files to Update: `utils/validators.py` and handlers

---

### 4. Database Query Optimization

#### Current Issues
- [ ] N+1 query problems possible
- [ ] No query result caching
- [ ] Missing database indexes on frequently queried columns

#### Improvements
```python
# In database/db.py - Add indexes
from sqlalchemy import Index

class Document(Base):
    __tablename__ = "documents"
    # ... fields ...
    
    __table_args__ = (
        Index('idx_user_id', 'user_id'),  # Speed up user lookups
        Index('idx_created_at', 'created_at'),  # Speed up date range queries
        Index('idx_document_type', 'document_type'),  # Speed up type filtering
    )

# Use eager loading for relationships
def get_user_with_documents(user_id: int, session):
    """Get user with all documents loaded efficiently."""
    from sqlalchemy.orm import joinedload
    
    user = session.query(User)\
        .options(joinedload(User.documents))\
        .filter(User.id == user_id)\
        .first()
    
    return user
```

#### Priority: 🔴 HIGH (for scalability)
#### Effort: Medium
#### Files to Update: `database/db.py`, `database/models.py`

---

### 5. API Response Consistency

#### Current Issues
- [ ] Inconsistent response structures
- [ ] No standard error response format
- [ ] Missing response status codes

#### Improvements
```python
# Create utils/responses.py - Standardize API responses

from typing import Any, Optional
from dataclasses import dataclass
from enum import Enum

class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"

@dataclass
class APIResponse:
    """Standard API response structure."""
    status: ResponseStatus
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "message": self.message,
            "data": self.data,
            "error_code": self.error_code,
        }

# Usage in handlers
async def handle_quiz_request(update, context):
    try:
        quiz = await quiz_service.generate_quiz(...)
        response = APIResponse(
            status=ResponseStatus.SUCCESS,
            message="Quiz generated successfully",
            data=quiz
        )
    except Exception as e:
        response = APIResponse(
            status=ResponseStatus.ERROR,
            message=str(e),
            error_code="QUIZ_GENERATION_FAILED"
        )
```

#### Priority: 🟡 MEDIUM
#### Effort: Medium
#### Files to Update: All handlers, create `utils/responses.py`

---

## Performance Optimizations

### 6. Caching Strategy

#### Current Issues
- [ ] No caching for frequently accessed data
- [ ] User settings fetched on every request
- [ ] Document embeddings regenerated unnecessarily

#### Improvements
```python
# In services/cache_service.py - Add caching layer

from functools import wraps
from datetime import datetime, timedelta
import hashlib

class CacheService:
    """Simple in-memory cache with TTL."""
    
    _cache = {}
    
    @staticmethod
    def set(key: str, value: Any, ttl_seconds: int = 3600):
        """Set cache value with TTL."""
        CacheService._cache[key] = {
            "value": value,
            "expires": datetime.now() + timedelta(seconds=ttl_seconds)
        }
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get cache value if not expired."""
        if key not in CacheService._cache:
            return None
        
        entry = CacheService._cache[key]
        if datetime.now() > entry["expires"]:
            del CacheService._cache[key]
            return None
        
        return entry["value"]
    
    @staticmethod
    def invalidate(pattern: str = None):
        """Invalidate cache entries matching pattern."""
        if pattern:
            keys_to_delete = [k for k in CacheService._cache if pattern in k]
            for key in keys_to_delete:
                del CacheService._cache[key]
        else:
            CacheService._cache.clear()

# Decorator for caching
def cached(ttl_seconds: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hashlib.md5(str(args+tuple(kwargs.items())).encode()).hexdigest()}"
            
            cached_value = CacheService.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            result = await func(*args, **kwargs)
            CacheService.set(cache_key, result, ttl_seconds)
            return result
        
        return wrapper
    return decorator

# Usage
@cached(ttl_seconds=1800)  # Cache for 30 minutes
async def get_user_settings(user_id: int):
    return session.query(UserSettings).filter_by(user_id=user_id).first()
```

#### Priority: 🔴 HIGH (for scalability)
#### Effort: Medium
#### Files to Create: `services/cache_service.py`

---

### 7. Async/Await Improvements

#### Current Issues
- [ ] Some I/O operations not properly async
- [ ] Potential blocking calls in async functions
- [ ] Missing concurrent operation handling

#### Improvements
```python
# ❌ Before - Blocking operation
async def process_multiple_files(file_paths):
    for file_path in file_paths:
        text = extract_text(file_path)  # Blocks here
        await process_text(text)

# ✅ After - Concurrent operations
import asyncio

async def process_multiple_files(file_paths):
    """Process multiple files concurrently."""
    tasks = [asyncio.to_thread(extract_text, fp) for fp in file_paths]
    texts = await asyncio.gather(*tasks)
    
    await asyncio.gather(*[process_text(t) for t in texts])
```

#### Priority: 🟡 MEDIUM
#### Effort: Medium
#### Files to Update: All services

---

### 8. Database Connection Pooling

#### Current Issues
- [ ] No connection pooling configured
- [ ] Potential connection leaks
- [ ] No max connection limits

#### Improvements
```python
# In database/db.py

from sqlalchemy.pool import QueuePool

# Configure connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # Minimum connections to keep
    max_overflow=20,  # Extra connections for overflow
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
)
```

#### Priority: 🔴 HIGH (for production)
#### Effort: Low
#### Files to Update: `database/db.py`

---

## Testing Improvements

### 9. Unit Test Coverage

#### Current Issues
- [ ] Limited test coverage (< 50%)
- [ ] Missing edge case tests
- [ ] No integration tests

#### Improvements
```python
# Add to tests/test_quiz_service.py

import pytest
from services.quiz_service import QuizService

@pytest.fixture
def quiz_service():
    return QuizService()

def test_generate_quiz_valid_content(quiz_service):
    """Test quiz generation with valid content."""
    content = "The Earth revolves around the Sun."
    quiz = quiz_service.generate_quiz(content, num_questions=1)
    
    assert len(quiz) == 1
    assert "question" in quiz[0]
    assert "options" in quiz[0]

def test_generate_quiz_empty_content(quiz_service):
    """Test quiz generation with empty content."""
    with pytest.raises(ValueError):
        quiz_service.generate_quiz("", num_questions=1)

def test_generate_quiz_invalid_difficulty(quiz_service):
    """Test quiz generation with invalid difficulty."""
    with pytest.raises(ValueError):
        quiz_service.generate_quiz(
            "Valid content",
            difficulty="invalid"
        )

def test_generate_quiz_max_questions():
    """Test that quiz respects max question limit."""
    quiz = quiz_service.generate_quiz("content", num_questions=100)
    assert len(quiz) <= 50  # Assuming max is 50
```

#### Priority: 🟡 MEDIUM
#### Effort: Medium
#### Files to Update: All test files in `tests/`

---

### 10. Integration Tests

#### Current Issues
- [ ] No end-to-end tests
- [ ] No API contract tests
- [ ] No database integration tests

#### Improvements
```python
# Add tests/test_integration.py

import pytest
from handlers.quiz import handle_quiz_request
from database.db import init_db

@pytest.fixture
def test_db():
    """Create test database."""
    init_db("sqlite:///:memory:")
    return session

@pytest.fixture
def test_user(test_db):
    """Create test user."""
    user = User(telegram_id=123, username="testuser")
    test_db.add(user)
    test_db.commit()
    return user

def test_quiz_flow_integration(test_user, test_db):
    """Test complete quiz generation flow."""
    # Create document
    doc = Document(
        user_id=test_user.id,
        content="The solar system contains 8 planets."
    )
    test_db.add(doc)
    test_db.commit()
    
    # Generate quiz
    quiz = quiz_service.generate_quiz(doc.content)
    
    assert len(quiz) > 0
    assert all("question" in q for q in quiz)
    
    # Save quiz
    quiz_record = Quiz(
        user_id=test_user.id,
        document_id=doc.id,
        questions=quiz
    )
    test_db.add(quiz_record)
    test_db.commit()
    
    # Verify saved
    assert test_db.query(Quiz).filter_by(user_id=test_user.id).count() == 1
```

#### Priority: 🟡 MEDIUM
#### Effort: High
#### Files to Create: `tests/test_integration.py`

---

## Documentation Improvements

### 11. API Documentation

#### Current Issues
- [ ] No formal API documentation
- [ ] Missing endpoint specifications
- [ ] No request/response examples

#### Improvements
```python
# Create ARCHITECTURE.md

# API Architecture

## Handlers Overview

### Quiz Handler - POST /api/quiz
Generate a quiz from document content.

**Request:**
```json
{
  "document_id": 123,
  "num_questions": 5,
  "difficulty": "medium",
  "question_type": "mcq"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "quiz_id": 456,
    "questions": [
      {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["Paris", "Lyon", "Marseille"],
        "correct_answer": 0
      }
    ]
  }
}
```

**Error Responses:**
- 400: Invalid parameters
- 404: Document not found
- 500: Internal server error
```

#### Priority: 🟡 MEDIUM
#### Effort: Medium
#### Files to Create: `ARCHITECTURE.md`

---

### 12. Code Comments & Docstrings

#### Current Issues
- [ ] Some functions lack docstrings
- [ ] Complex logic not well commented
- [ ] No explanation of design decisions

#### Improvements
```python
# ❌ Before
def calculate_ease_factor(quality, ease_factor):
    return max(1.3, ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

# ✅ After
def calculate_ease_factor(quality: int, ease_factor: float) -> float:
    """
    Calculate the ease factor for SM-2 spaced repetition algorithm.
    
    The ease factor determines how quickly a flashcard will be reviewed.
    It increases with correct answers and decreases with incorrect ones.
    
    Args:
        quality: Rating from 0-5 where:
            - 0-2: Incorrect answer
            - 3-5: Correct answer (varying difficulty)
        ease_factor: Current ease factor (default usually 2.5)
    
    Returns:
        Updated ease factor, clamped between 1.3 and infinity
    
    Reference:
        https://en.wikipedia.org/wiki/SuperMemo#Algorithm_SM-2
    
    Example:
        >>> calculate_ease_factor(4, 2.5)
        2.36
    """
    return max(
        1.3,  # Minimum ease factor
        ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    )
```

#### Priority: 🟡 MEDIUM
#### Effort: Low
#### Files to Update: All source files

---

## Deployment & DevOps

### 13. Environment Configuration

#### Current Issues
- [ ] Limited environment separation
- [ ] No production vs development configs
- [ ] Secrets not properly managed

#### Improvements
```python
# Create config/settings.py

from enum import Enum
import os

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings:
    """Application settings based on environment."""
    
    ENV = Environment(os.getenv("APP_ENV", "development"))
    DEBUG = ENV == Environment.DEVELOPMENT
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///study_assistant.db"
    )
    
    # API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Logging
    LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
    
    # Features
    ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() == "true"
    ENABLE_SPACED_REPETITION = os.getenv("ENABLE_SPACED_REPETITION", "true").lower() == "true"
    
    # Limits
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_QUIZ_QUESTIONS = 50
    MAX_CONCURRENT_REQUESTS = 100
    
    @classmethod
    def validate(cls):
        """Validate required settings."""
        if not cls.OPENAI_API_KEY and not cls.GOOGLE_API_KEY:
            raise ValueError("Either OPENAI_API_KEY or GOOGLE_API_KEY must be set")
```

#### Priority: 🟠 MEDIUM
#### Effort: Low
#### Files to Create: `config/settings.py`

---

## Security Improvements

### 14. Input Sanitization

#### Current Issues
- [ ] Potential SQL injection (mitigated by ORM but could be explicit)
- [ ] Limited XSS prevention
- [ ] No rate limiting

#### Improvements
```python
# In utils/security.py

import re
from typing import str

def sanitize_user_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Raw user input
        max_length: Maximum allowed length
    
    Returns:
        Sanitized text
    """
    # Limit length
    text = text[:max_length]
    
    # Remove potentially dangerous patterns
    text = re.sub(r'[<>\"\'%;)(&+]', '', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def add_rate_limiting(max_requests: int = 100, window: int = 3600):
    """Decorator for rate limiting."""
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context):
            user_id = update.effective_user.id
            key = f"rate_limit:{func.__name__}:{user_id}"
            
            # Check rate limit
            count = cache.get(key) or 0
            if count >= max_requests:
                await update.message.reply_text(
                    f"⏸️ Rate limit exceeded. Try again in {window//60} minutes."
                )
                return
            
            # Increment counter
            cache.set(key, count + 1, ttl_seconds=window)
            
            return await func(update, context)
        
        return wrapper
    return decorator
```

#### Priority: 🔴 HIGH
#### Effort: Medium
#### Files to Create: `utils/security.py`

---

## Implementation Priority Summary

| Improvement | Priority | Effort | Impact |
|------------|----------|--------|--------|
| Error Handling | 🔴 HIGH | Medium | High |
| Type Hints | 🟡 MEDIUM | Low | Medium |
| Input Validation | 🟡 MEDIUM | Low-Medium | High |
| Database Optimization | 🔴 HIGH | Medium | Very High |
| Response Consistency | 🟡 MEDIUM | Medium | Medium |
| Caching Strategy | 🔴 HIGH | Medium | Very High |
| Async Improvements | 🟡 MEDIUM | Medium | High |
| Connection Pooling | 🔴 HIGH | Low | High |
| Unit Tests | 🟡 MEDIUM | Medium | High |
| Integration Tests | 🟡 MEDIUM | High | Medium |
| API Documentation | 🟡 MEDIUM | Medium | High |
| Code Comments | 🟡 MEDIUM | Low | Medium |
| Environment Config | 🟠 MEDIUM | Low | Medium |
| Security | 🔴 HIGH | Medium | Very High |

---

## Next Steps

1. **Week 1**: Implement error handling and security improvements
2. **Week 2**: Add database optimization and caching
3. **Week 3**: Improve test coverage
4. **Week 4**: Documentation and code cleanup

See [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines.
