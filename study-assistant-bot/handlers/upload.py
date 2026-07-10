"""
Document Upload Handler
"""

from telegram import Update, ParseMode
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from utils.logger import get_logger

logger = get_logger(__name__)


async def upload_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle upload callbacks."""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("📤 Upload feature coming soon!")


async def handle_document_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads."""
    await update.message.reply_text("📤 Document upload feature coming soon!")
