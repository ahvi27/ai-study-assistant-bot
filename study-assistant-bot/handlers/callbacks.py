"""Callback query handler."""
from telegram import Update
from telegram.ext import ContextTypes
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Feature coming soon!")
