"""Ask handler."""
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import get_logger
logger = get_logger(__name__)

async def ask_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("❓ Ask feature coming soon!")
