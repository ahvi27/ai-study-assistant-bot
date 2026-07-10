"""Flashcard handler."""
from telegram import Update
from telegram.ext import ContextTypes
async def flashcard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("🎴 Flashcard feature coming soon!")
