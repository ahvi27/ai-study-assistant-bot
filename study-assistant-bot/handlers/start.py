"""
Start command handler for Study Assistant Bot.
"""

import logging
from telegram import Update, ParseMode
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from keyboards.main_menu import get_main_menu
from database.db import get_session, UserDB
from utils.logger import get_logger

logger = get_logger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    try:
        user = update.effective_user
        chat_id = update.effective_chat.id

        # Send typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

        # Get or create user in database
        session = get_session()
        db_user = UserDB.create_user(
            session,
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        session.close()

        welcome_message = f"""🎓 Welcome to *Study Assistant Bot*!

Hello {user.first_name}! I'm your personal AI-powered study companion.

📚 *What I can help you with:*
• 💬 Chat with AI about any topic
• 📤 Upload and manage study materials
• ❓ Ask questions about your documents
• 🧠 Generate quizzes and test yourself
• 🎴 Create flashcards for memorization
• 📝 Summarize and translate notes
• 📊 Track your study progress
• ⏰ Set study reminders
• 📋 Get personalized study plans

Let's get started! Tap a button below or type /help"""

        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu(),
        )

        logger.info(f"User {user.id} started bot")

    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ An error occurred. Please try again.",
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    try:
        chat_id = update.effective_chat.id

        help_message = """*Study Assistant Bot - Help* ❓

*Available Commands:*

/start - Start the bot and show main menu
/help - Show this help message
/chat - Start a conversation with AI
/upload - Upload a study document
/ask - Ask a question about your notes
/quiz - Generate a quiz
/flashcards - Create flashcards
/summary - Summarize your notes
/translate - Translate content
/plan - Create a study plan
/remind - Set study reminders
/progress - View your progress
/settings - Modify settings

*Quick Guide:*

1. *Upload Documents* - Upload PDFs, DOCX, or TXT files
2. *Ask Questions* - Get AI answers based on your notes
3. *Take Quizzes* - Test yourself with AI-generated quizzes
4. *Manage Flashcards* - Create and study flashcards
5. *Track Progress* - View your study statistics

*Supported Languages:*
English, French, Spanish, Arabic, Amharic, German, Italian, Portuguese, Japanese, Chinese

*Tips:*
• Upload notes first for better personalized help
• Use /progress to track your learning
• Set reminders to maintain consistency
• Try different quiz difficulties

Need more help? Feel free to ask!"""

        await context.bot.send_message(
            chat_id=chat_id,
            text=help_message,
            parse_mode="Markdown",
        )

        logger.info(f"User {update.effective_user.id} requested help")

    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ An error occurred displaying help.",
        )



