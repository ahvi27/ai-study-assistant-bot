"""Help command handler."""

from telegram import Update, ParseMode
from telegram.ext import ContextTypes
from utils.logger import get_logger

logger = get_logger(__name__)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
*Study Assistant Bot - Commands*

/start - Start the bot
/help - Show this message
/menu - Show main menu

*Features:*
📤 Upload notes (PDF, DOCX, TXT)
❓ Ask questions about your notes
🧠 Generate quizzes
🎴 Create flashcards
📝 Summarize notes
🌐 Translate content
📊 View progress
⏰ Set reminders
📋 Create study plans

Use the buttons below for more!
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
