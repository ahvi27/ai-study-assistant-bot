"""
Main menu keyboard for Study Assistant Bot.
Provides inline buttons for all main features.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config


def get_main_menu() -> InlineKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("💬 Chat with AI", callback_data="chat"),
            InlineKeyboardButton("📚 Upload Notes", callback_data="upload"),
        ],
        [
            InlineKeyboardButton("❓ Ask Question", callback_data="ask_question"),
            InlineKeyboardButton("🧪 Take Quiz", callback_data="quiz"),
        ],
        [
            InlineKeyboardButton("🎯 Flashcards", callback_data="flashcards"),
            InlineKeyboardButton("📊 Progress", callback_data="progress"),
        ],
        [
            InlineKeyboardButton("📝 Summary", callback_data="summary"),
            InlineKeyboardButton("🌐 Translate", callback_data="translate"),
        ],
        [
            InlineKeyboardButton("📅 Study Plan", callback_data="study_plan"),
            InlineKeyboardButton("⏰ Reminders", callback_data="reminders"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_quiz_options() -> InlineKeyboardMarkup:
    """Get quiz type selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("Multiple Choice (MCQ)", callback_data="quiz_mcq")],
        [InlineKeyboardButton("True/False", callback_data="quiz_true_false")],
        [InlineKeyboardButton("Short Answer", callback_data="quiz_short_answer")],
        [InlineKeyboardButton("Mixed Questions", callback_data="quiz_mixed")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_difficulty_selection() -> InlineKeyboardMarkup:
    """Get difficulty level selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="diff_easy")],
        [InlineKeyboardButton("Medium", callback_data="diff_medium")],
        [InlineKeyboardButton("Hard", callback_data="diff_hard")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_summary_options() -> InlineKeyboardMarkup:
    """Get summary type selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("Short Summary", callback_data="summary_short")],
        [InlineKeyboardButton("Bullet Points", callback_data="summary_bullet")],
        [InlineKeyboardButton("Medium Summary", callback_data="summary_medium")],
        [InlineKeyboardButton("Long Summary", callback_data="summary_long")],
        [InlineKeyboardButton("Study Guide", callback_data="summary_study_guide")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_language_selection() -> InlineKeyboardMarkup:
    """Get language selection keyboard"""
    languages = [
        ("English", "en"),
        ("French", "fr"),
        ("Spanish", "es"),
        ("Arabic", "ar"),
        ("Amharic", "am"),
        ("German", "de"),
        ("Italian", "it"),
        ("Portuguese", "pt"),
        ("Japanese", "ja"),
        ("Chinese", "zh"),
    ]

    keyboard = []
    for i in range(0, len(languages), 2):
        row = []
        row.append(InlineKeyboardButton(languages[i][0], callback_data=f"lang_{languages[i][1]}"))
        if i + 1 < len(languages):
            row.append(InlineKeyboardButton(languages[i + 1][0], callback_data=f"lang_{languages[i + 1][1]}"))
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("« Back", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)


def get_reminder_type_selection() -> InlineKeyboardMarkup:
    """Get reminder type selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("Daily Reminder", callback_data="reminder_daily")],
        [InlineKeyboardButton("Weekly Reminder", callback_data="reminder_weekly")],
        [InlineKeyboardButton("Custom Reminder", callback_data="reminder_custom")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_yes_no_keyboard() -> InlineKeyboardMarkup:
    """Get yes/no confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data="yes"),
            InlineKeyboardButton("❌ No", callback_data="no"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Get cancel keyboard"""
    keyboard = [
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Get back button keyboard"""
    keyboard = [
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_pagination_keyboard(current_page: int, total_pages: int, prefix: str = "page") -> InlineKeyboardMarkup:
    """
    Get pagination keyboard

    Args:
        current_page: Current page number
        total_pages: Total number of pages
        prefix: Callback data prefix

    Returns:
        Pagination keyboard
    """
    keyboard = []

    # Previous button
    row = []
    if current_page > 1:
        row.append(InlineKeyboardButton("« Previous", callback_data=f"{prefix}_{current_page - 1}"))
    else:
        row.append(InlineKeyboardButton(" ", callback_data="no_op"))

    # Page indicator
    row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="no_op"))

    # Next button
    if current_page < total_pages:
        row.append(InlineKeyboardButton("Next »", callback_data=f"{prefix}_{current_page + 1}"))
    else:
        row.append(InlineKeyboardButton(" ", callback_data="no_op"))

    keyboard.append(row)
    keyboard.append([InlineKeyboardButton("« Back", callback_data="back_to_main")])

    return InlineKeyboardMarkup(keyboard)


def get_quiz_action_keyboard() -> InlineKeyboardMarkup:
    """Get quiz action keyboard"""
    keyboard = [
        [InlineKeyboardButton("📋 View Answers", callback_data="quiz_answers")],
        [InlineKeyboardButton("📊 View Score", callback_data="quiz_score")],
        [InlineKeyboardButton("🔄 Try Again", callback_data="quiz_retry")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_document_actions() -> InlineKeyboardMarkup:
    """Get document action keyboard"""
    keyboard = [
        [InlineKeyboardButton("❓ Ask Question", callback_data="doc_ask")],
        [InlineKeyboardButton("📝 Summarize", callback_data="doc_summary")],
        [InlineKeyboardButton("🎯 Create Quiz", callback_data="doc_quiz")],
        [InlineKeyboardButton("🎴 Make Flashcards", callback_data="doc_flashcards")],
        [InlineKeyboardButton("❌ Delete", callback_data="doc_delete")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_question_count_selection() -> InlineKeyboardMarkup:
    """Get question count selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("5 Questions", callback_data="q_count_5")],
        [InlineKeyboardButton("10 Questions", callback_data="q_count_10")],
        [InlineKeyboardButton("15 Questions", callback_data="q_count_15")],
        [InlineKeyboardButton("20 Questions", callback_data="q_count_20")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_flashcard_action_keyboard(total_cards: int = 0) -> InlineKeyboardMarkup:
    """
    Get flashcard action keyboard

    Args:
        total_cards: Total number of flashcards

    Returns:
        Flashcard action keyboard
    """
    keyboard = [
        [
            InlineKeyboardButton("◀️ Previous", callback_data="fc_previous"),
            InlineKeyboardButton("Show Answer", callback_data="fc_show_answer"),
            InlineKeyboardButton("Next ▶️", callback_data="fc_next"),
        ],
        [
            InlineKeyboardButton("✅ Correct", callback_data="fc_correct"),
            InlineKeyboardButton("❌ Incorrect", callback_data="fc_incorrect"),
        ],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_settings_menu() -> InlineKeyboardMarkup:
    """Get settings menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌐 Language", callback_data="settings_language")],
        [InlineKeyboardButton("⏰ Timezone", callback_data="settings_timezone")],
        [InlineKeyboardButton("📊 Statistics", callback_data="settings_stats")],
        [InlineKeyboardButton("🗑️ Clear Data", callback_data="settings_clear")],
        [InlineKeyboardButton("« Back", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)
