"""
Tests for AI Service
"""

import unittest
from unittest.mock import patch, MagicMock
from services.ai_service import AIService, OpenAIProvider, GeminiProvider


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAI Provider"""

    def setUp(self):
        """Set up test fixtures"""
        with patch.dict("os.environ", {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_MODEL": "gpt-4-turbo-preview",
        }):
            self.provider = OpenAIProvider()

    @patch("openai.ChatCompletion.create")
    def test_generate_text(self, mock_create):
        """Test text generation"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response

        result = self.provider.generate_text("Test prompt")

        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, str))

    @patch("openai.ChatCompletion.create")
    def test_generate_text_with_system_prompt(self, mock_create):
        """Test text generation with system prompt"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response

        result = self.provider.generate_text(
            "User prompt",
            system_prompt="You are helpful"
        )

        self.assertIsNotNone(result)
        mock_create.assert_called_once()

    @patch("openai.ChatCompletion.create")
    def test_generate_text_error_handling(self, mock_create):
        """Test error handling"""
        mock_create.side_effect = Exception("API Error")

        result = self.provider.generate_text("Test prompt")

        self.assertIsNone(result)


class TestAIService(unittest.TestCase):
    """Test AI Service"""

    def test_answer_question(self):
        """Test question answering"""
        service = AIService()

        # Mock the provider
        with patch.object(service, "provider") as mock_provider:
            mock_provider.generate_text.return_value = "The answer is..."

            result = service.answer_question("What is AI?")

            self.assertIsNotNone(result)
            self.assertTrue(isinstance(result, str))

    def test_answer_question_with_context(self):
        """Test question answering with context"""
        service = AIService()

        with patch.object(service, "provider") as mock_provider:
            mock_provider.generate_text.return_value = "Based on the context..."

            result = service.answer_question(
                "What is the main topic?",
                context="This document discusses..."
            )

            self.assertIsNotNone(result)

    def test_summarize_text(self):
        """Test text summarization"""
        service = AIService()

        with patch.object(service, "provider") as mock_provider:
            mock_provider.generate_text.return_value = "Summary of the text"

            result = service.summarize_text("Long text to summarize")

            self.assertIsNotNone(result)

    def test_summarize_text_different_lengths(self):
        """Test summarization with different lengths"""
        service = AIService()

        with patch.object(service, "provider") as mock_provider:
            mock_provider.generate_text.return_value = "Summary"

            for length in ["short", "medium", "long"]:
                result = service.summarize_text("Text", length=length)
                self.assertIsNotNone(result)

    def test_translate_text(self):
        """Test text translation"""
        service = AIService()

        with patch.object(service, "provider") as mock_provider:
            mock_provider.generate_text.return_value = "Traducción"

            result = service.translate_text(
                "Hello",
                target_language="Spanish"
            )

            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
