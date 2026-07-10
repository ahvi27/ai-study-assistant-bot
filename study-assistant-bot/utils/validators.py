"""
Input Validation and Sanitization Utilities
"""

import re
from config import Config
from utils.logger import logger


def validate_file_size(file_size_bytes: int) -> tuple[bool, str]:
    """
    Validate uploaded file size

    Args:
        file_size_bytes: Size of file in bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    max_size_bytes = Config.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if file_size_bytes > max_size_bytes:
        return (
            False,
            f"File size exceeds maximum limit of {Config.MAX_UPLOAD_SIZE_MB}MB",
        )

    if file_size_bytes == 0:
        return False, "File is empty"

    return True, ""


def validate_file_type(filename: str) -> tuple[bool, str]:
    """
    Validate file type based on extension

    Args:
        filename: Name of the file

    Returns:
        Tuple of (is_valid, error_message)
    """
    allowed_extensions = {".pdf", ".docx", ".txt"}

    file_extension = "." + filename.split(".")[-1].lower()

    if file_extension not in allowed_extensions:
        return (
            False,
            f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
        )

    return True, ""


def validate_text_input(text: str, min_length: int = 1, max_length: int = 4000) -> tuple[bool, str]:
    """
    Validate text input

    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Message cannot be empty"

    text = text.strip()

    if len(text) < min_length:
        return False, f"Message must be at least {min_length} characters"

    if len(text) > max_length:
        return False, f"Message must not exceed {max_length} characters"

    return True, ""


def sanitize_text(text: str) -> str:
    """
    Sanitize user input text

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = " ".join(text.split())

    # Remove potentially harmful characters (keep alphanumeric, spaces, and basic punctuation)
    text = re.sub(r"[^\w\s\.\,\!\?\-\'\"\(\):/]", "", text)

    return text


def validate_quiz_difficulty(difficulty: str) -> tuple[bool, str]:
    """
    Validate quiz difficulty level

    Args:
        difficulty: Difficulty level

    Returns:
        Tuple of (is_valid, error_message)
    """
    if difficulty.lower() not in Config.QUIZ_DIFFICULTY_LEVELS:
        valid_levels = ", ".join(Config.QUIZ_DIFFICULTY_LEVELS)
        return False, f"Invalid difficulty. Valid options: {valid_levels}"

    return True, ""


def validate_language_code(language_code: str) -> tuple[bool, str]:
    """
    Validate language code

    Args:
        language_code: Language code

    Returns:
        Tuple of (is_valid, error_message)
    """
    if language_code.lower() not in Config.SUPPORTED_LANGUAGES:
        valid_languages = ", ".join(Config.SUPPORTED_LANGUAGES.keys())
        return (
            False,
            f"Unsupported language. Valid options: {valid_languages}",
        )

    return True, ""


def validate_date_format(date_string: str) -> tuple[bool, str]:
    """
    Validate date format (YYYY-MM-DD)

    Args:
        date_string: Date string

    Returns:
        Tuple of (is_valid, error_message)
    """
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"

    if not re.match(date_pattern, date_string):
        return False, "Invalid date format. Use YYYY-MM-DD"

    return True, ""


def validate_integer(value: str, min_val: int = None, max_val: int = None) -> tuple[bool, str, int]:
    """
    Validate and convert string to integer

    Args:
        value: String value
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Tuple of (is_valid, error_message, converted_value)
    """
    try:
        int_value = int(value)

        if min_val is not None and int_value < min_val:
            return False, f"Value must be at least {min_val}", 0

        if max_val is not None and int_value > max_val:
            return False, f"Value must not exceed {max_val}", 0

        return True, "", int_value

    except ValueError:
        return False, "Invalid number format", 0
