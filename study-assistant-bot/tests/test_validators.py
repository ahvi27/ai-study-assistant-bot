"""
Tests for Validators
"""

import unittest
from utils.validators import (
    validate_file_size,
    validate_file_type,
    validate_text_input,
    sanitize_text,
    validate_quiz_difficulty,
    validate_language_code,
    validate_date_format,
    validate_integer,
)


class TestFileValidators(unittest.TestCase):
    """Test file validation functions"""

    def test_validate_file_size_valid(self):
        """Test valid file size"""
        is_valid, msg = validate_file_size(5 * 1024 * 1024)  # 5MB
        self.assertTrue(is_valid)

    def test_validate_file_size_too_large(self):
        """Test file size exceeds limit"""
        is_valid, msg = validate_file_size(30 * 1024 * 1024)  # 30MB
        self.assertFalse(is_valid)
        self.assertIn("exceeds", msg)

    def test_validate_file_size_empty(self):
        """Test empty file"""
        is_valid, msg = validate_file_size(0)
        self.assertFalse(is_valid)

    def test_validate_file_type_pdf(self):
        """Test PDF file type"""
        is_valid, msg = validate_file_type("document.pdf")
        self.assertTrue(is_valid)

    def test_validate_file_type_docx(self):
        """Test DOCX file type"""
        is_valid, msg = validate_file_type("document.docx")
        self.assertTrue(is_valid)

    def test_validate_file_type_invalid(self):
        """Test invalid file type"""
        is_valid, msg = validate_file_type("document.exe")
        self.assertFalse(is_valid)


class TestTextValidators(unittest.TestCase):
    """Test text validation functions"""

    def test_validate_text_input_valid(self):
        """Test valid text input"""
        is_valid, msg = validate_text_input("This is a valid question")
        self.assertTrue(is_valid)

    def test_validate_text_input_empty(self):
        """Test empty text input"""
        is_valid, msg = validate_text_input("")
        self.assertFalse(is_valid)

    def test_validate_text_input_too_short(self):
        """Test text too short"""
        is_valid, msg = validate_text_input("Hi")
        self.assertFalse(is_valid)

    def test_validate_text_input_too_long(self):
        """Test text too long"""
        text = "a" * 5000
        is_valid, msg = validate_text_input(text)
        self.assertFalse(is_valid)

    def test_sanitize_text(self):
        """Test text sanitization"""
        text = "Hello   World  !!!"
        sanitized = sanitize_text(text)
        self.assertEqual(sanitized, "Hello World !")

    def test_sanitize_text_with_special_chars(self):
        """Test sanitization with special characters"""
        text = "Test<script>alert('xss')</script>"
        sanitized = sanitize_text(text)
        self.assertNotIn("<script>", sanitized)


class TestQuizValidators(unittest.TestCase):
    """Test quiz-related validators"""

    def test_validate_quiz_difficulty_valid(self):
        """Test valid quiz difficulty"""
        is_valid, msg = validate_quiz_difficulty("easy")
        self.assertTrue(is_valid)

        is_valid, msg = validate_quiz_difficulty("medium")
        self.assertTrue(is_valid)

        is_valid, msg = validate_quiz_difficulty("hard")
        self.assertTrue(is_valid)

    def test_validate_quiz_difficulty_invalid(self):
        """Test invalid quiz difficulty"""
        is_valid, msg = validate_quiz_difficulty("impossible")
        self.assertFalse(is_valid)


class TestLanguageValidators(unittest.TestCase):
    """Test language validators"""

    def test_validate_language_code_valid(self):
        """Test valid language codes"""
        is_valid, msg = validate_language_code("en")
        self.assertTrue(is_valid)

        is_valid, msg = validate_language_code("es")
        self.assertTrue(is_valid)

    def test_validate_language_code_invalid(self):
        """Test invalid language code"""
        is_valid, msg = validate_language_code("xyz")
        self.assertFalse(is_valid)


class TestDateValidators(unittest.TestCase):
    """Test date validators"""

    def test_validate_date_format_valid(self):
        """Test valid date format"""
        is_valid, msg = validate_date_format("2024-12-25")
        self.assertTrue(is_valid)

    def test_validate_date_format_invalid(self):
        """Test invalid date format"""
        is_valid, msg = validate_date_format("25/12/2024")
        self.assertFalse(is_valid)

        is_valid, msg = validate_date_format("2024-13-01")
        self.assertFalse(is_valid)


class TestIntegerValidators(unittest.TestCase):
    """Test integer validators"""

    def test_validate_integer_valid(self):
        """Test valid integer"""
        is_valid, msg, value = validate_integer("42")
        self.assertTrue(is_valid)
        self.assertEqual(value, 42)

    def test_validate_integer_with_min(self):
        """Test integer with minimum value"""
        is_valid, msg, value = validate_integer("5", min_val=10)
        self.assertFalse(is_valid)

    def test_validate_integer_with_max(self):
        """Test integer with maximum value"""
        is_valid, msg, value = validate_integer("15", max_val=10)
        self.assertFalse(is_valid)

    def test_validate_integer_invalid(self):
        """Test invalid integer"""
        is_valid, msg, value = validate_integer("not_a_number")
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
