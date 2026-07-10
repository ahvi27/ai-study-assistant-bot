"""Reminder handler."""
from telegram import Update
from telegram.ext import ContextTypes
async def reminder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("⏰ Reminder feature coming soon!")
