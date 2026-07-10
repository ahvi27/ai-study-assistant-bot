"""
Flashcard Service
Generate and manage flashcards
"""

from typing import List, Dict, Optional
from services.ai_service import AIService
from utils.logger import logger


class FlashcardService:
    """Service for generating and managing flashcards"""

    def __init__(self):
        """Initialize flashcard service"""
        self.ai_service = AIService()

    def generate_flashcards(
        self,
        content: str,
        num_cards: int = 10,
        difficulty: str = "medium",
        language: str = "English",
    ) -> Optional[List[Dict]]:
        """
        Generate flashcards from content

        Args:
            content: Content to create flashcards from
            num_cards: Number of flashcards to generate
            difficulty: Difficulty level
            language: Language for questions

        Returns:
            List of flashcard dictionaries or None
        """
        try:
            prompt = f"""Create {num_cards} flashcards ({difficulty} difficulty) from the following content.
Each flashcard should have a question on the front and answer on the back.
Make questions clear and answers concise (1-3 sentences).

Content:
{content}

Respond with a JSON array where each item has:
- "question": question text (front of card)
- "answer": answer text (back of card)
- "difficulty": "{difficulty}"
- "category": topic/category of the flashcard

Return ONLY valid JSON array."""

            system_prompt = f"You are an expert educator creating effective flashcards in {language}."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response and isinstance(response, list):
                return response

            return None

        except Exception as e:
            logger.error(f"Error generating flashcards: {e}")
            return None

    def generate_vocabulary_flashcards(
        self,
        content: str,
        num_cards: int = 10,
        language: str = "English",
    ) -> Optional[List[Dict]]:
        """
        Generate vocabulary flashcards

        Args:
            content: Content to extract vocabulary from
            num_cards: Number of flashcards
            language: Language

        Returns:
            List of vocabulary flashcards
        """
        try:
            prompt = f"""Extract {num_cards} important vocabulary terms from the following content.
Create flashcards for each term with definition and example usage.

Content:
{content}

Respond with JSON array where each item has:
- "term": the vocabulary word/term
- "definition": clear definition
- "example": example sentence using the term
- "difficulty": "easy", "medium", or "hard"
- "part_of_speech": noun, verb, adjective, etc.

Return ONLY valid JSON array."""

            system_prompt = f"You are an expert educator creating vocabulary flashcards in {language}."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response and isinstance(response, list):
                # Reformat to match standard flashcard format
                flashcards = []
                for item in response:
                    flashcards.append({
                        "question": f"Define: {item.get('term', '')}",
                        "answer": f"{item.get('definition', '')}\n\nExample: {item.get('example', '')}",
                        "term": item.get("term", ""),
                        "part_of_speech": item.get("part_of_speech", ""),
                        "difficulty": item.get("difficulty", "medium"),
                        "category": "Vocabulary",
                    })
                return flashcards

            return None

        except Exception as e:
            logger.error(f"Error generating vocabulary flashcards: {e}")
            return None

    def generate_concept_flashcards(
        self,
        content: str,
        num_cards: int = 10,
    ) -> Optional[List[Dict]]:
        """
        Generate concept-based flashcards

        Args:
            content: Content to create flashcards from
            num_cards: Number of flashcards

        Returns:
            List of concept flashcards
        """
        try:
            prompt = f"""Create {num_cards} concept flashcards from the following content.
Focus on main ideas, definitions, and relationships between concepts.

Content:
{content}

Respond with JSON array where each item has:
- "concept": the main concept
- "definition": definition of the concept
- "related_concepts": list of related concepts
- "key_points": list of 2-3 key points about this concept
- "difficulty": "easy", "medium", or "hard"

Return ONLY valid JSON array."""

            system_prompt = "You are an expert educator identifying and explaining key concepts."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response and isinstance(response, list):
                flashcards = []
                for item in response:
                    key_points_text = "\n".join([f"• {p}" for p in item.get("key_points", [])])
                    related_text = ", ".join(item.get("related_concepts", []))

                    flashcards.append({
                        "question": f"Explain: {item.get('concept', '')}",
                        "answer": f"{item.get('definition', '')}\n\nKey Points:\n{key_points_text}\n\nRelated: {related_text}",
                        "concept": item.get("concept", ""),
                        "difficulty": item.get("difficulty", "medium"),
                        "category": "Concepts",
                    })
                return flashcards

            return None

        except Exception as e:
            logger.error(f"Error generating concept flashcards: {e}")
            return None

    def generate_qa_flashcards(
        self,
        content: str,
        num_cards: int = 10,
    ) -> Optional[List[Dict]]:
        """
        Generate question-answer flashcards

        Args:
            content: Content to create Q&A from
            num_cards: Number of flashcards

        Returns:
            List of Q&A flashcards
        """
        try:
            prompt = f"""Create {num_cards} question-answer flashcards from the following content.
Make questions specific and answers detailed but concise.

Content:
{content}

Respond with JSON array where each item has:
- "question": specific question about the content
- "answer": detailed but concise answer
- "difficulty": "easy", "medium", or "hard"
- "topic": topic/category

Return ONLY valid JSON array."""

            system_prompt = "You are an expert educator creating effective question-answer flashcards."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response and isinstance(response, list):
                for item in response:
                    item["category"] = "Q&A"
                return response

            return None

        except Exception as e:
            logger.error(f"Error generating Q&A flashcards: {e}")
            return None

    def format_flashcard_for_display(self, flashcard: Dict, show_answer: bool = False) -> str:
        """
        Format flashcard for Telegram display

        Args:
            flashcard: Flashcard dictionary
            show_answer: Whether to show answer

        Returns:
            Formatted text for display
        """
        try:
            difficulty = flashcard.get("difficulty", "medium").upper()
            category = flashcard.get("category", "General")

            text = f"""📇 Flashcard
Category: {category} | Difficulty: {difficulty}

*Question:*
{flashcard.get('question', '')}
"""

            if show_answer:
                text += f"""
*Answer:*
{flashcard.get('answer', '')}
"""

            return text

        except Exception as e:
            logger.error(f"Error formatting flashcard: {e}")
            return "Error displaying flashcard"

    def get_review_statistics(self, flashcards: List[Dict]) -> Dict:
        """
        Get review statistics for flashcards

        Args:
            flashcards: List of flashcard data

        Returns:
            Statistics dictionary
        """
        try:
            total_cards = len(flashcards)
            reviewed = sum(1 for fc in flashcards if fc.get("times_reviewed", 0) > 0)
            correct = sum(fc.get("times_correct", 0) for fc in flashcards)
            total_reviews = sum(fc.get("times_reviewed", 0) for fc in flashcards)

            accuracy = (correct / total_reviews * 100) if total_reviews > 0 else 0

            by_difficulty = {
                "easy": sum(1 for fc in flashcards if fc.get("difficulty") == "easy"),
                "medium": sum(1 for fc in flashcards if fc.get("difficulty") == "medium"),
                "hard": sum(1 for fc in flashcards if fc.get("difficulty") == "hard"),
            }

            return {
                "total_cards": total_cards,
                "cards_reviewed": reviewed,
                "cards_pending": total_cards - reviewed,
                "total_reviews": total_reviews,
                "total_correct": correct,
                "accuracy": round(accuracy, 2),
                "by_difficulty": by_difficulty,
            }

        except Exception as e:
            logger.error(f"Error calculating review statistics: {e}")
            return {}

    def get_due_flashcards(self, flashcards: List[Dict], limit: int = 5) -> List[Dict]:
        """
        Get flashcards due for review

        Args:
            flashcards: List of flashcards
            limit: Maximum number to return

        Returns:
            List of flashcards due for review
        """
        try:
            due = []

            for fc in flashcards:
                # If never reviewed, it's due
                if fc.get("times_reviewed", 0) == 0:
                    due.append(fc)
                    if len(due) >= limit:
                        return due

            # Sort by last review time for spaced repetition
            due.sort(key=lambda x: x.get("last_reviewed", "1970-01-01"))

            return due[:limit]

        except Exception as e:
            logger.error(f"Error getting due flashcards: {e}")
            return []

    def get_statistics_summary(self, flashcards: List[Dict]) -> str:
        """
        Generate text summary of flashcard statistics

        Args:
            flashcards: List of flashcards

        Returns:
            Summary text
        """
        try:
            stats = self.get_review_statistics(flashcards)

            summary = f"""
📊 Flashcard Statistics
{'=' * 40}
Total Cards: {stats.get('total_cards', 0)}
Cards Reviewed: {stats.get('cards_reviewed', 0)}
Cards Pending: {stats.get('cards_pending', 0)}

Total Reviews: {stats.get('total_reviews', 0)}
Total Correct: {stats.get('total_correct', 0)}
Accuracy: {stats.get('accuracy', 0)}%

By Difficulty:
  Easy: {stats.get('by_difficulty', {}).get('easy', 0)}
  Medium: {stats.get('by_difficulty', {}).get('medium', 0)}
  Hard: {stats.get('by_difficulty', {}).get('hard', 0)}
"""
            return summary.strip()

        except Exception as e:
            logger.error(f"Error generating statistics summary: {e}")
            return "Error generating statistics"
