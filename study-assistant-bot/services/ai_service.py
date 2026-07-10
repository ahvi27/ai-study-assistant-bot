"""
AI Service module for Study Assistant Bot.
Handles all AI operations using OpenAI API.
"""

import logging
from typing import Optional, List, Dict
from openai import OpenAI, APIError
from config import Config

logger = logging.getLogger(__name__)


class AIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize AI service with OpenAI client."""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.embedding_model = Config.OPENAI_EMBEDDING_MODEL
        self.max_tokens = Config.OPENAI_MAX_TOKENS
        self.timeout = Config.OPENAI_TIMEOUT
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = None,
    ) -> Optional[str]:
        """Generate text response from AI model."""
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or self.max_tokens,
                timeout=self.timeout,
            )
            
            return response.choices[0].message.content
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return "I encountered an error while processing your request. Please try again."
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text using OpenAI."""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text,
                timeout=self.timeout,
            )
            return response.data[0].embedding
        except APIError as e:
            logger.error(f"OpenAI API error generating embedding: {e}")
            return None
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def generate_quiz(
        self,
        content: str,
        num_questions: int = 5,
        difficulty: str = "medium",
    ) -> Optional[List[dict]]:
        """Generate quiz questions from content."""
        try:
            prompt = f"""Generate {num_questions} multiple choice quiz questions at {difficulty} difficulty level based on this content:

{content}

Format your response as a JSON array with this structure:
[
  {{
    "question": "Question text",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Why this is correct"
  }}
]

Only return the JSON array, no other text."""
            
            response = self.generate_response(
                prompt,
                temperature=0.5,
                max_tokens=2000,
            )
            
            if response:
                import json
                try:
                    quiz_data = json.loads(response)
                    return quiz_data
                except json.JSONDecodeError:
                    logger.error("Failed to parse quiz JSON response")
                    return None
            
            return None
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return None
    
    def generate_flashcards(
        self,
        content: str,
        num_cards: int = 10,
    ) -> Optional[List[dict]]:
        """Generate flashcards from content."""
        try:
            prompt = f"""Generate {num_cards} flashcards (question-answer pairs) based on this content:

{content}

Format your response as a JSON array with this structure:
[
  {{
    "question": "Question text",
    "answer": "Answer text",
    "difficulty": "easy|medium|hard"
  }}
]

Only return the JSON array, no other text."""
            
            response = self.generate_response(
                prompt,
                temperature=0.5,
                max_tokens=2000,
            )
            
            if response:
                import json
                try:
                    flashcards = json.loads(response)
                    return flashcards
                except json.JSONDecodeError:
                    logger.error("Failed to parse flashcards JSON response")
                    return None
            
            return None
        except Exception as e:
            logger.error(f"Error generating flashcards: {e}")
            return None
    
    def summarize_content(
        self,
        content: str,
        summary_type: str = "short",
    ) -> Optional[str]:
        """Summarize content."""
        try:
            length_instructions = {
                "short": "2-3 sentences",
                "detailed": "1-2 paragraphs",
                "bullet": "bullet points (5-7 bullets)",
            }
            
            length = length_instructions.get(summary_type, "short")
            
            prompt = f"""Summarize the following content in {length}:

{content}

Provide only the summary, no additional text."""
            
            return self.generate_response(
                prompt,
                temperature=0.5,
                max_tokens=1000,
            )
        except Exception as e:
            logger.error(f"Error summarizing content: {e}")
            return None
    
    def translate_text(
        self,
        text: str,
        target_language: str,
    ) -> Optional[str]:
        """Translate text to target language."""
        try:
            prompt = f"""Translate the following text to {target_language}:

{text}

Provide only the translation, no additional text."""
            
            return self.generate_response(
                prompt,
                temperature=0.3,
                max_tokens=2000,
            )
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return None
    
    def generate_study_plan(
        self,
        subjects: List[str],
        exam_date: str,
        daily_hours: float,
    ) -> Optional[dict]:
        """Generate personalized study plan."""
        try:
            subjects_str = ", ".join(subjects)
            
            prompt = f"""Generate a detailed personalized study plan for a student with these parameters:
- Subjects: {subjects_str}
- Exam Date: {exam_date}
- Daily Study Hours Available: {daily_hours}

Create a structured daily breakdown as a JSON object with:
- week_1, week_2, etc. (keys)
- Each week containing daily_plan array with subjects to study each day
- Each day having: subject, topics, focus_areas

Format as JSON only, no other text."""
            
            response = self.generate_response(
                prompt,
                temperature=0.5,
                max_tokens=3000,
            )
            
            if response:
                import json
                try:
                    plan = json.loads(response)
                    return plan
                except json.JSONDecodeError:
                    logger.error("Failed to parse study plan JSON response")
                    return None
            
            return None
        except Exception as e:
            logger.error(f"Error generating study plan: {e}")
            return None
    
    def answer_question(
        self,
        question: str,
        context: str = None,
    ) -> Optional[str]:
        """Answer a question, optionally using provided context."""
        try:
            if context:
                system_prompt = f"""You are a knowledgeable study assistant. Use the provided context to answer questions accurately and helpfully.

Context:
{context}"""
                prompt = question
            else:
                system_prompt = "You are a knowledgeable study assistant. Answer questions accurately and helpfully."
                prompt = question
            
            return self.generate_response(
                prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1500,
            )
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return None
