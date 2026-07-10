"""
Summary Service
Generate various types of summaries from content
"""

from typing import Optional, Dict
from services.ai_service import AIService
from utils.logger import logger


class SummaryService:
    """Service for generating summaries"""

    def __init__(self):
        """Initialize summary service"""
        self.ai_service = AIService()

    def generate_short_summary(self, content: str) -> Optional[str]:
        """
        Generate short summary (2-3 sentences)

        Args:
            content: Content to summarize

        Returns:
            Summary text or None
        """
        try:
            prompt = f"""Summarize the following text in 2-3 sentences, capturing the main ideas:

{content}

Summary:"""

            system_prompt = "You are an expert at creating concise, accurate summaries."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=500,
            )

        except Exception as e:
            logger.error(f"Error generating short summary: {e}")
            return None

    def generate_medium_summary(self, content: str) -> Optional[str]:
        """
        Generate medium summary (1 paragraph)

        Args:
            content: Content to summarize

        Returns:
            Summary text or None
        """
        try:
            prompt = f"""Summarize the following text in one comprehensive paragraph (100-200 words):

{content}

Summary:"""

            system_prompt = "You are an expert at creating well-structured, informative summaries."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=800,
            )

        except Exception as e:
            logger.error(f"Error generating medium summary: {e}")
            return None

    def generate_long_summary(self, content: str) -> Optional[str]:
        """
        Generate long summary (3-4 paragraphs)

        Args:
            content: Content to summarize

        Returns:
            Summary text or None
        """
        try:
            prompt = f"""Summarize the following text in 3-4 detailed paragraphs (300-400 words), covering:
1. Main topic and purpose
2. Key concepts and ideas
3. Supporting details
4. Conclusion

{content}

Summary:"""

            system_prompt = "You are an expert at creating detailed, comprehensive summaries."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=1500,
            )

        except Exception as e:
            logger.error(f"Error generating long summary: {e}")
            return None

    def generate_bullet_summary(self, content: str, num_points: int = 5) -> Optional[str]:
        """
        Generate bullet point summary

        Args:
            content: Content to summarize
            num_points: Number of bullet points

        Returns:
            Summary text or None
        """
        try:
            prompt = f"""Create {num_points} key bullet points summarizing the main ideas from this text:

{content}

Requirements:
- Each bullet should be 1-2 sentences
- Use clear, concise language
- Focus on key concepts and takeaways
- Format as bullet points

Key Points:"""

            system_prompt = "You are an expert at extracting and summarizing key points."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=800,
            )

        except Exception as e:
            logger.error(f"Error generating bullet summary: {e}")
            return None

    def generate_outline_summary(self, content: str) -> Optional[str]:
        """
        Generate outline-style summary

        Args:
            content: Content to summarize

        Returns:
            Summary text or None
        """
        try:
            prompt = f"""Create a hierarchical outline summarizing the key information:

{content}

Format as:
1. Main Topic
   a. Subtopic 1
      i. Supporting detail
   b. Subtopic 2
      i. Supporting detail
2. Main Topic 2
   ...

Only include the most important information."""

            system_prompt = "You are an expert at creating clear, well-organized outlines."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=1000,
            )

        except Exception as e:
            logger.error(f"Error generating outline summary: {e}")
            return None

    def generate_key_concepts(self, content: str, num_concepts: int = 5) -> Optional[str]:
        """
        Extract key concepts and definitions

        Args:
            content: Content to analyze
            num_concepts: Number of concepts

        Returns:
            Formatted concepts or None
        """
        try:
            prompt = f"""Identify and explain the top {num_concepts} key concepts from this text:

{content}

For each concept:
1. Write the concept name
2. Write a 1-2 sentence explanation
3. Provide an example or application

Format clearly."""

            system_prompt = "You are an expert at identifying and explaining key concepts."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=1000,
            )

        except Exception as e:
            logger.error(f"Error extracting key concepts: {e}")
            return None

    def generate_executive_summary(self, content: str) -> Optional[str]:
        """
        Generate executive summary for professionals

        Args:
            content: Content to summarize

        Returns:
            Executive summary or None
        """
        try:
            prompt = f"""Create a professional executive summary that:
1. States the main topic/purpose
2. Lists 3-5 key findings or points
3. Provides actionable recommendations or conclusions
4. Is suitable for a busy professional (2-3 paragraphs max)

Content:
{content}

Executive Summary:"""

            system_prompt = "You are an expert at creating concise executive summaries for professionals."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=1000,
            )

        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return None

    def generate_study_guide(self, content: str) -> Optional[str]:
        """
        Generate a study guide from content

        Args:
            content: Content to create study guide from

        Returns:
            Study guide or None
        """
        try:
            prompt = f"""Create a comprehensive study guide from this content with:

1. **Overview**: Brief introduction to the topic
2. **Key Terms**: Main vocabulary with definitions
3. **Main Concepts**: Important ideas explained
4. **Important Facts**: Critical information to memorize
5. **Practice Questions**: 3-5 questions to test understanding
6. **Study Tips**: Suggestions for learning this material

Content:
{content}

Study Guide:"""

            system_prompt = "You are an expert educator creating effective study guides."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=2000,
            )

        except Exception as e:
            logger.error(f"Error generating study guide: {e}")
            return None

    def compare_summaries(self, content: str) -> Optional[Dict[str, str]]:
        """
        Generate multiple summary types for comparison

        Args:
            content: Content to summarize

        Returns:
            Dictionary with different summary types
        """
        try:
            summaries = {
                "short": self.generate_short_summary(content),
                "bullet": self.generate_bullet_summary(content, num_points=3),
                "medium": self.generate_medium_summary(content),
            }

            return summaries if any(summaries.values()) else None

        except Exception as e:
            logger.error(f"Error comparing summaries: {e}")
            return None

    def estimate_reading_time(self, content: str) -> int:
        """
        Estimate reading time in minutes

        Args:
            content: Content to analyze

        Returns:
            Estimated reading time in minutes
        """
        try:
            # Average reading speed is ~200-250 words per minute
            words = len(content.split())
            minutes = max(1, round(words / 225))
            return minutes

        except Exception:
            return 1

    def get_summary_statistics(self, content: str) -> Dict:
        """
        Get statistics about content

        Args:
            content: Content to analyze

        Returns:
            Dictionary with statistics
        """
        try:
            words = content.split()
            sentences = content.split(".")
            paragraphs = content.split("\n\n")

            return {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "average_word_length": sum(len(w) for w in words) / len(words) if words else 0,
                "estimated_reading_time": self.estimate_reading_time(content),
            }

        except Exception as e:
            logger.error(f"Error getting summary statistics: {e}")
            return {}
