"""
Helper Utilities and Common Functions
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from utils.logger import logger
import json


def format_message(text: str, bold: bool = False, italic: bool = False, code: bool = False) -> str:
    """
    Format text with Markdown styling for Telegram

    Args:
        text: Text to format
        bold: Make text bold
        italic: Make text italic
        code: Format as code

    Returns:
        Formatted text
    """
    if code:
        return f"`{text}`"
    if bold:
        return f"*{text}*"
    if italic:
        return f"_{text}_"
    return text


def create_progress_bar(current: int, total: int, width: int = 10) -> str:
    """
    Create a progress bar string

    Args:
        current: Current progress
        total: Total value
        width: Width of progress bar

    Returns:
        Progress bar string
    """
    if total == 0:
        return "█" * width

    percentage = (current / total) * 100
    filled = int((percentage / 100) * width)
    empty = width - filled

    bar = "█" * filled + "░" * empty
    return f"{bar} {percentage:.1f}%"


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks

    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    if chunk_size <= 0 or overlap < 0:
        return [text]

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def truncate_text(text: str, max_length: int = 4000, suffix: str = "...") -> str:
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def escape_markdown(text: str) -> str:
    """
    Escape special Markdown characters

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    special_chars = r"_*[]()~`>#+-=|{}.!"
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text


def parse_duration(duration_str: str) -> Optional[timedelta]:
    """
    Parse duration string (e.g., '1h', '30m', '2d')

    Args:
        duration_str: Duration string

    Returns:
        Timedelta object or None if invalid
    """
    duration_str = duration_str.lower().strip()

    multipliers = {
        "m": 60,  # minutes
        "h": 60 * 60,  # hours
        "d": 24 * 60 * 60,  # days
        "w": 7 * 24 * 60 * 60,  # weeks
    }

    try:
        for unit, multiplier in multipliers.items():
            if duration_str.endswith(unit):
                value = int(duration_str[:-1])
                return timedelta(seconds=value * multiplier)
    except (ValueError, IndexError):
        pass

    return None


def get_readable_duration(seconds: int) -> str:
    """
    Convert seconds to readable duration string

    Args:
        seconds: Number of seconds

    Returns:
        Readable duration string
    """
    if seconds < 60:
        return f"{seconds}s"

    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"

    hours = minutes // 60
    if hours < 24:
        return f"{hours}h {minutes % 60}m"

    days = hours // 24
    return f"{days}d {hours % 24}h"


def calculate_study_streak(last_study_date: Optional[datetime]) -> int:
    """
    Calculate current study streak

    Args:
        last_study_date: Last date user studied

    Returns:
        Number of consecutive days
    """
    if not last_study_date:
        return 0

    today = datetime.now().date()
    last_date = last_study_date.date() if isinstance(last_study_date, datetime) else last_study_date

    if (today - last_date).days == 0:
        return 1
    elif (today - last_date).days > 1:
        return 0

    return 1


def get_time_of_day_greeting() -> str:
    """
    Get appropriate greeting based on time of day

    Returns:
        Greeting message
    """
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning! ☀️"
    elif 12 <= hour < 17:
        return "Good afternoon! 🌤️"
    elif 17 <= hour < 21:
        return "Good evening! 🌆"
    else:
        return "Good night! 🌙"


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime for display

    Args:
        dt: Datetime object

    Returns:
        Formatted string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def safe_dict_get(data: Dict, key: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value

    Args:
        data: Dictionary
        key: Key (supports dot notation for nesting)
        default: Default value if key not found

    Returns:
        Value or default
    """
    keys = key.split(".")
    current = data

    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default

    return current


def split_text_by_lines(text: str, max_lines: int = 10) -> List[str]:
    """
    Split text into chunks by number of lines

    Args:
        text: Text to split
        max_lines: Maximum lines per chunk

    Returns:
        List of text chunks
    """
    lines = text.split("\n")
    chunks = []
    current_chunk = []

    for line in lines:
        current_chunk.append(line)
        if len(current_chunk) >= max_lines:
            chunks.append("\n".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


def json_serialize(obj: Any) -> str:
    """
    Safely serialize object to JSON

    Args:
        obj: Object to serialize

    Returns:
        JSON string
    """
    try:
        return json.dumps(obj, default=str)
    except Exception as e:
        logger.error(f"JSON serialization error: {e}")
        return "{}"


def parse_json_safely(json_str: str, default: Any = None) -> Any:
    """
    Safely parse JSON string

    Args:
        json_str: JSON string
        default: Default value if parsing fails

    Returns:
        Parsed object or default
    """
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"JSON parsing error: {e}")
        return default
