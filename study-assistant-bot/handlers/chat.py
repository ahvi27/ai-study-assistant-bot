"""Chat handler."""

from telegram import Update, ParseMode
from telegram.ext import ContextTypes
from utils.logger import get_logger

logger = get_logger(__name__)


async def chat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle chat callback."""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("💬 Chat feature coming soon!")


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages."""
    await update.message.reply_text("💬 Chat feature coming soon!")
