# 🎯 Quick Implementation Guide - High Priority Features

This guide provides actionable steps to implement high-priority features from [FUTURE_FEATURES.md](FUTURE_FEATURES.md).

## Feature 1: Spaced Repetition for Flashcards ⭐ HIGH PRIORITY

### What It Does
Automatically schedules flashcards for review based on the SM-2 algorithm, showing each card at optimal intervals.

### Files to Modify
- `database/models.py` - Add fields to Flashcard model
- `services/flashcard_service.py` - Add spaced repetition logic
- `handlers/flashcard.py` - Update review flow

### Implementation Steps

#### Step 1: Update Database Model
Add these fields to the `Flashcard` model in `database/models.py`:

```python
class Flashcard(Base):
    # ... existing fields ...
    
    # Spaced repetition fields
    last_reviewed = Column(DateTime, nullable=True)
    next_review = Column(DateTime, nullable=True)
    ease_factor = Column(Float, default=2.5)  # SM-2 ease factor
    interval = Column(Integer, default=1)  # Days between reviews
    repetitions = Column(Integer, default=0)  # Number of reviews
    difficulty = Column(Integer, default=0)  # 0-5 quality rating
```

#### Step 2: Create Spaced Repetition Service
Create `services/spaced_repetition_service.py`:

```python
from datetime import datetime, timedelta
from math import exp

class SpacedRepetitionService:
    """SM-2 algorithm implementation for spaced repetition."""
    
    @staticmethod
    def calculate_next_review(flashcard, quality: int):
        """
        Calculate next review date using SM-2 algorithm.
        
        Args:
            flashcard: Flashcard object
            quality: User's rating (0-5)
                0-2: Incorrect
                3-5: Correct (varying difficulty)
        """
        if quality < 3:
            # Reset if incorrect
            flashcard.interval = 1
            flashcard.repetitions = 0
        else:
            if flashcard.repetitions == 0:
                flashcard.interval = 1
            elif flashcard.repetitions == 1:
                flashcard.interval = 3
            else:
                flashcard.interval = round(
                    flashcard.interval * flashcard.ease_factor
                )
            flashcard.repetitions += 1
        
        # Update ease factor
        flashcard.ease_factor = max(
            1.3,
            flashcard.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        )
        
        flashcard.last_reviewed = datetime.now()
        flashcard.next_review = datetime.now() + timedelta(days=flashcard.interval)
        
        return flashcard
    
    @staticmethod
    def get_due_flashcards(user_id: int, session):
        """Get all flashcards due for review."""
        from database.models import Flashcard
        
        now = datetime.now()
        return session.query(Flashcard).filter(
            Flashcard.user_id == user_id,
            (Flashcard.next_review == None) | (Flashcard.next_review <= now)
        ).all()
```

#### Step 3: Update Flashcard Handler
Modify `handlers/flashcard.py` to implement review flow:

```python
# Add to flashcard handler
async def review_flashcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start flashcard review session."""
    user_id = update.effective_user.id
    
    # Get due flashcards
    due_cards = SpacedRepetitionService.get_due_flashcards(user_id, session)
    
    if not due_cards:
        await update.message.reply_text(
            "✅ No flashcards to review right now!\n"
            "You're all caught up! 🎉"
        )
        return
    
    # Show first card
    card = due_cards[0]
    context.user_data['current_card'] = card.id
    context.user_data['review_queue'] = [c.id for c in due_cards]
    
    await show_flashcard(update, context, card)
```

### Expected Outcome
✅ Flashcards appear when they're due for review
✅ Automatic scheduling based on performance
✅ Better long-term retention

---

## Feature 2: Quiz Difficulty Levels ⭐ HIGH PRIORITY

### What It Does
Generate quizzes at Easy, Medium, and Hard difficulty levels with appropriate question complexity.

### Files to Modify
- `services/quiz_service.py` - Add difficulty logic
- `handlers/quiz.py` - Add difficulty selection UI

### Implementation Steps

#### Step 1: Update Quiz Service
Modify `services/quiz_service.py`:

```python
DIFFICULTY_PROMPTS = {
    "easy": """Generate EASY multiple choice questions. 
    - Obvious correct answers
    - Simple vocabulary
    - Direct facts from text
    - Clear distractors""",
    
    "medium": """Generate MEDIUM difficulty questions.
    - Require understanding of concepts
    - Intermediate vocabulary
    - Combine multiple ideas
    - Plausible wrong answers""",
    
    "hard": """Generate HARD difficulty questions.
    - Require critical thinking
    - Advanced concepts
    - Inference and analysis needed
    - Tricky similar options"""
}

async def generate_quiz_with_difficulty(
    content: str,
    num_questions: int = 5,
    difficulty: str = "medium"
) -> List[dict]:
    """Generate quiz with specified difficulty level."""
    
    if difficulty not in DIFFICULTY_PROMPTS:
        difficulty = "medium"
    
    prompt = f"""
    {DIFFICULTY_PROMPTS[difficulty]}
    
    Create {num_questions} MCQ questions from:
    {content}
    """
    
    # Call AI to generate questions
    response = await ai_service.generate_text(prompt)
    return parse_quiz_questions(response)
```

#### Step 2: Update Quiz Handler
Modify `handlers/quiz.py`:

```python
async def start_quiz_wizard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start quiz with difficulty selection."""
    
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="quiz_easy")],
        [InlineKeyboardButton("Medium", callback_data="quiz_medium")],
        [InlineKeyboardButton("Hard", callback_data="quiz_hard")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📚 Select quiz difficulty:\n\n"
        "🟢 Easy - Great for beginners\n"
        "🟡 Medium - Good review\n"
        "🔴 Hard - Test mastery",
        reply_markup=reply_markup
    )
```

### Expected Outcome
✅ Users can choose difficulty level
✅ Quizzes match user's skill level
✅ Better learning progression

---

## Feature 3: Achievement & Badges System ⭐ HIGH PRIORITY

### What It Does
Reward users with badges for reaching milestones, encouraging continued engagement.

### Files to Modify
- `database/models.py` - Add Badge model
- `services/achievement_service.py` - Create new service
- `handlers/progress.py` - Display badges

### Implementation Steps

#### Step 1: Add Badge Model
Add to `database/models.py`:

```python
class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_type = Column(String, nullable=False)  # "streak_7", "flashcards_100", etc.
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'badge_type', name='uq_user_badge'),
    )

BADGES = {
    "first_step": {
        "name": "First Step",
        "emoji": "👶",
        "description": "Complete first quiz",
        "trigger": lambda stats: stats['quizzes_completed'] >= 1
    },
    "streak_7": {
        "name": "Weekly Warrior",
        "emoji": "🔥",
        "description": "7-day study streak",
        "trigger": lambda stats: stats['current_streak'] >= 7
    },
    "streak_30": {
        "name": "Study Master",
        "emoji": "🏆",
        "description": "30-day study streak",
        "trigger": lambda stats: stats['current_streak'] >= 30
    },
    "flashcards_100": {
        "name": "Card Collector",
        "emoji": "🎴",
        "description": "Create 100 flashcards",
        "trigger": lambda stats: stats['flashcards_created'] >= 100
    },
    "quiz_perfect": {
        "name": "Perfectionist",
        "emoji": "⭐",
        "description": "Score 100% on a quiz",
        "trigger": lambda stats: stats['perfect_quizzes'] >= 1
    },
}
```

#### Step 2: Create Achievement Service
Create `services/achievement_service.py`:

```python
class AchievementService:
    
    @staticmethod
    async def check_and_award_badges(user_id: int, session):
        """Check if user earned any new badges."""
        
        # Get user stats
        stats = await get_user_stats(user_id, session)
        
        # Get already earned badges
        earned = session.query(Badge).filter_by(user_id=user_id).all()
        earned_types = {b.badge_type for b in earned}
        
        # Check each badge
        new_badges = []
        for badge_type, badge_info in BADGES.items():
            if badge_type not in earned_types:
                if badge_info['trigger'](stats):
                    badge = Badge(user_id=user_id, badge_type=badge_type)
                    session.add(badge)
                    new_badges.append(badge_info)
        
        if new_badges:
            session.commit()
        
        return new_badges
```

#### Step 3: Update Progress Handler
Modify `handlers/progress.py`:

```python
async def show_badges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display user's earned badges."""
    user_id = update.effective_user.id
    
    badges = session.query(Badge).filter_by(user_id=user_id).all()
    
    message = "🏆 Your Achievements\n\n"
    if not badges:
        message += "No badges earned yet. Keep studying! 📚"
    else:
        for badge in badges:
            info = BADGES[badge.badge_type]
            message += f"{info['emoji']} {info['name']}\n"
            message += f"   {info['description']}\n\n"
    
    await update.message.reply_text(message)
```

### Expected Outcome
✅ Users see badges for achievements
✅ Motivational rewards system
✅ Better user engagement

---

## Feature 4: OCR - Image Text Recognition ⭐ HIGH PRIORITY

### What It Does
Extract text from images so users can create flashcards from photos of notes or textbooks.

### Files to Modify
- `services/ocr_service.py` - Create new service
- `handlers/upload.py` - Add image support

### Implementation Steps

#### Step 1: Install OCR Library
```bash
pip install pytesseract pillow
# Also install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
```

#### Step 2: Create OCR Service
Create `services/ocr_service.py`:

```python
import pytesseract
from PIL import Image
from typing import Optional

class OCRService:
    """Extract text from images using Tesseract."""
    
    @staticmethod
    async def extract_text_from_image(image_path: str) -> Optional[str]:
        """Extract text from image file."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            if not text.strip():
                logger.warning(f"No text found in {image_path}")
                return None
            
            return text
        except Exception as e:
            logger.error(f"OCR Error: {e}")
            return None
    
    @staticmethod
    async def extract_and_create_flashcards(
        image_path: str,
        user_id: int,
        session
    ) -> Optional[List]:
        """Extract text and automatically create flashcards."""
        
        text = await OCRService.extract_text_from_image(image_path)
        
        if not text:
            return None
        
        # Use flashcard service to generate from extracted text
        flashcards = await flashcard_service.generate_flashcards(
            text, 
            user_id,
            session
        )
        
        return flashcards
```

#### Step 3: Update Upload Handler
Modify `handlers/upload.py`:

```python
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo uploads for OCR."""
    
    user_id = update.effective_user.id
    file = await update.message.photo[-1].get_file()
    
    # Download image
    image_path = f"storage/uploads/{user_id}_photo.jpg"
    await file.download_to_drive(image_path)
    
    # Extract text
    text = await OCRService.extract_text_from_image(image_path)
    
    if not text:
        await update.message.reply_text("❌ No text found in image")
        return
    
    # Offer options
    keyboard = [
        [InlineKeyboardButton("Create Flashcards", callback_data="ocr_flashcards")],
        [InlineKeyboardButton("Summarize", callback_data="ocr_summary")],
        [InlineKeyboardButton("Generate Quiz", callback_data="ocr_quiz")],
    ]
    
    context.user_data['extracted_text'] = text
    
    await update.message.reply_text(
        "📸 Text extracted from image!\n"
        "What would you like to do?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
```

### Expected Outcome
✅ Users can upload photos of notes
✅ Automatic text extraction from images
✅ Quick flashcard creation from photos

---

## Quick Implementation Checklist

```
📋 Spaced Repetition
  [ ] Add database fields
  [ ] Create service
  [ ] Update handler
  [ ] Test with sample cards
  
🎲 Quiz Difficulty
  [ ] Update quiz service
  [ ] Add UI buttons
  [ ] Test different difficulties
  
🏆 Achievements
  [ ] Create badge model
  [ ] Create achievement service
  [ ] Update progress handler
  [ ] Test badge logic
  
📸 OCR Support
  [ ] Install tesseract
  [ ] Create OCR service
  [ ] Update upload handler
  [ ] Test with sample images
```

---

## Testing These Features

### Test Spaced Repetition
```python
# In test_spaced_repetition.py
from services.spaced_repetition_service import SpacedRepetitionService

def test_sm2_calculation():
    card = Flashcard(ease_factor=2.5, interval=1, repetitions=0)
    card = SpacedRepetitionService.calculate_next_review(card, quality=4)
    assert card.repetitions == 1
    assert card.interval == 3
```

### Test Quiz Difficulty
```python
# Test that hard questions are actually harder
hard_quiz = await quiz_service.generate_quiz_with_difficulty(content, difficulty="hard")
easy_quiz = await quiz_service.generate_quiz_with_difficulty(content, difficulty="easy")
# Verify hard quiz has longer answers (more complex)
```

### Test Achievement System
```python
# Verify badges are awarded correctly
stats = {'current_streak': 7}
badges = check_and_award_badges(user_id, stats)
assert any(b['badge_type'] == 'streak_7' for b in badges)
```

---

## What's Next?

After implementing these features, consider:
1. **Group Study** - Enable users to share flashcards
2. **Teacher Dashboard** - Create class management features
3. **API Development** - Build REST API for third-party access

See [FUTURE_FEATURES.md](FUTURE_FEATURES.md) for the complete roadmap.
