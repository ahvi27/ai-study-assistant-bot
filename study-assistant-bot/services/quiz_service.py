"""
Quiz Generation Service
Create quizzes from documents or general topics
"""

from typing import List, Dict, Optional
import json
from services.ai_service import AIService
from utils.logger import logger


class QuizService:
    """Service for generating and managing quizzes"""

    def __init__(self):
        """Initialize quiz service"""
        self.ai_service = AIService()

    def generate_mcq_quiz(
        self,
        content: str,
        num_questions: int = 5,
        difficulty: str = "medium",
    ) -> Optional[Dict]:
        """
        Generate Multiple Choice Questions (MCQ) quiz

        Args:
            content: Content to create questions from
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)

        Returns:
            Dictionary with quiz questions or None
        """
        try:
            difficulty_instructions = {
                "easy": "Create simple questions about basic concepts. Include obvious incorrect answers.",
                "medium": "Create questions that require understanding of the content. Mix easy and harder concepts.",
                "hard": "Create challenging questions that require deep understanding and critical thinking.",
            }

            prompt = f"""Create {num_questions} multiple choice questions ({difficulty} difficulty) from the following content.

{difficulty_instructions.get(difficulty, '')}

Content:
{content}

Respond with a JSON array where each item has:
- "question": the question text
- "options": array of 4 options (strings)
- "correct_answer": index of correct option (0-3)
- "explanation": brief explanation of the correct answer

Return ONLY valid JSON, no other text."""

            system_prompt = "You are an expert educator creating high-quality quiz questions."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response and isinstance(response, list):
                return {
                    "type": "mcq",
                    "difficulty": difficulty,
                    "questions": response,
                    "num_questions": len(response),
                }

            return None

        except Exception as e:
            logger.error(f"Error generating MCQ quiz: {e}")
            return None

    def generate_true_false_quiz(
        self,
        content: str,
        num_questions: int = 5,
        difficulty: str = "medium",
    ) -> Optional[Dict]:
        """
        Generate True/False quiz

        Args:
            content: Content to create questions from
            num_questions: Number of questions
            difficulty: Difficulty level

        Returns:
            Dictionary with quiz questions or None
        """
        try:
            prompt = f"""Create {num_questions} true/false questions ({difficulty} difficulty) from the following content.

Content:
{content}

Respond with a JSON array where each item has:
- "statement": the statement (should be ambiguous enough to trick)
- "answer": true or false
- "explanation": explanation of why the answer is correct

Return ONLY valid JSON."""

            system_prompt = "You are an expert educator creating true/false questions that test understanding."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response and isinstance(response, list):
                return {
                    "type": "true_false",
                    "difficulty": difficulty,
                    "questions": response,
                    "num_questions": len(response),
                }

            return None

        except Exception as e:
            logger.error(f"Error generating True/False quiz: {e}")
            return None

    def generate_short_answer_quiz(
        self,
        content: str,
        num_questions: int = 5,
        difficulty: str = "medium",
    ) -> Optional[Dict]:
        """
        Generate short answer questions

        Args:
            content: Content to create questions from
            num_questions: Number of questions
            difficulty: Difficulty level

        Returns:
            Dictionary with quiz questions or None
        """
        try:
            prompt = f"""Create {num_questions} short answer questions ({difficulty} difficulty) from the following content.

Content:
{content}

Respond with a JSON array where each item has:
- "question": the question text
- "ideal_answer": ideal/sample answer (1-2 sentences)
- "keywords": array of keywords that should appear in correct answer
- "points": points for this question (1-5)

Return ONLY valid JSON."""

            system_prompt = "You are an expert educator creating short answer questions that test understanding and retention."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response and isinstance(response, list):
                return {
                    "type": "short_answer",
                    "difficulty": difficulty,
                    "questions": response,
                    "num_questions": len(response),
                }

            return None

        except Exception as e:
            logger.error(f"Error generating short answer quiz: {e}")
            return None

    def generate_mixed_quiz(
        self,
        content: str,
        difficulty: str = "medium",
    ) -> Optional[Dict]:
        """
        Generate a mixed quiz with different question types

        Args:
            content: Content to create questions from
            difficulty: Difficulty level

        Returns:
            Dictionary with mixed questions or None
        """
        try:
            # Generate 3 MCQ, 2 True/False
            mcq = self.generate_mcq_quiz(content, num_questions=3, difficulty=difficulty)
            tf = self.generate_true_false_quiz(content, num_questions=2, difficulty=difficulty)

            if mcq and tf:
                return {
                    "type": "mixed",
                    "difficulty": difficulty,
                    "sections": [
                        {
                            "name": "Multiple Choice",
                            "type": "mcq",
                            "questions": mcq.get("questions", []),
                        },
                        {
                            "name": "True/False",
                            "type": "true_false",
                            "questions": tf.get("questions", []),
                        },
                    ],
                    "num_questions": len(mcq.get("questions", [])) + len(tf.get("questions", [])),
                }

            return None

        except Exception as e:
            logger.error(f"Error generating mixed quiz: {e}")
            return None

    def evaluate_mcq_answer(
        self,
        question: Dict,
        user_answer_index: int,
    ) -> Dict:
        """
        Evaluate MCQ answer

        Args:
            question: Question dictionary
            user_answer_index: Index of user's selected option

        Returns:
            Evaluation result
        """
        try:
            correct_index = question.get("correct_answer", -1)
            is_correct = user_answer_index == correct_index

            return {
                "is_correct": is_correct,
                "correct_answer_index": correct_index,
                "correct_answer": question.get("options", [])[correct_index] if correct_index >= 0 else "",
                "explanation": question.get("explanation", ""),
                "user_selected_index": user_answer_index,
            }

        except Exception as e:
            logger.error(f"Error evaluating MCQ answer: {e}")
            return {"is_correct": False, "error": str(e)}

    def evaluate_true_false_answer(
        self,
        question: Dict,
        user_answer: bool,
    ) -> Dict:
        """
        Evaluate True/False answer

        Args:
            question: Question dictionary
            user_answer: User's answer (True/False)

        Returns:
            Evaluation result
        """
        try:
            correct_answer = question.get("answer", False)
            is_correct = user_answer == correct_answer

            return {
                "is_correct": is_correct,
                "correct_answer": correct_answer,
                "user_answer": user_answer,
                "explanation": question.get("explanation", ""),
            }

        except Exception as e:
            logger.error(f"Error evaluating True/False answer: {e}")
            return {"is_correct": False, "error": str(e)}

    def evaluate_short_answer(
        self,
        question: Dict,
        user_answer: str,
    ) -> Dict:
        """
        Evaluate short answer (AI-powered)

        Args:
            question: Question dictionary
            user_answer: User's answer

        Returns:
            Evaluation result
        """
        try:
            keywords = question.get("keywords", [])
            ideal_answer = question.get("ideal_answer", "")

            prompt = f"""Evaluate if this student answer is correct based on the ideal answer and keywords.

Question: {question.get('question', '')}

Ideal Answer: {ideal_answer}

Important Keywords: {', '.join(keywords)}

Student Answer: {user_answer}

Respond with JSON containing:
- "is_correct": boolean (true if answer captures main concepts)
- "score": out of {question.get('points', 5)}
- "feedback": brief feedback on the answer
- "keywords_found": array of keywords found in student answer

Return ONLY valid JSON."""

            system_prompt = "You are an expert educator evaluating student answers fairly and constructively."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response:
                return response

            return {
                "is_correct": False,
                "score": 0,
                "feedback": "Could not evaluate answer",
            }

        except Exception as e:
            logger.error(f"Error evaluating short answer: {e}")
            return {"is_correct": False, "score": 0, "error": str(e)}

    def calculate_score(self, results: List[Dict]) -> Dict:
        """
        Calculate quiz score from evaluation results

        Args:
            results: List of question results

        Returns:
            Score summary
        """
        try:
            total_questions = len(results)
            correct_answers = sum(1 for r in results if r.get("is_correct", False))
            percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

            return {
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "incorrect_answers": total_questions - correct_answers,
                "percentage": round(percentage, 2),
                "grade": self._get_grade(percentage),
            }

        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return {"error": str(e)}

    @staticmethod
    def _get_grade(percentage: float) -> str:
        """Get letter grade from percentage"""
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"

    def generate_quiz_summary(self, quiz_data: Dict, results: List[Dict]) -> Optional[str]:
        """
        Generate text summary of quiz performance

        Args:
            quiz_data: Quiz data
            results: Quiz results

        Returns:
            Summary text or None
        """
        try:
            score_summary = self.calculate_score(results)

            summary = f"""
📊 Quiz Summary
{'=' * 40}
Total Questions: {score_summary.get('total_questions', 0)}
Correct Answers: {score_summary.get('correct_answers', 0)}
Incorrect Answers: {score_summary.get('incorrect_answers', 0)}
Percentage: {score_summary.get('percentage', 0)}%
Grade: {score_summary.get('grade', 'N/A')}

Difficulty: {quiz_data.get('difficulty', 'N/A').upper()}
Quiz Type: {quiz_data.get('type', 'N/A').replace('_', ' ').title()}
"""
            return summary.strip()

        except Exception as e:
            logger.error(f"Error generating quiz summary: {e}")
            return None
