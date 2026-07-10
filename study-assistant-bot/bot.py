#!/usr/bin/env python3
"""
Study Assistant Telegram Bot - Main Entry Point
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from database.db import init_db
from utils.logger import logger
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, PicklePersistence
from telegram import Update
from telegram.ext import ContextTypes


def setup_handlers(app: Application):
    """Setup all command and message handlers."""
    
    # Command handlers - start
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from handlers.start import handle_start
        await handle_start(update, context)
    
    app.add_handler(CommandHandler("start", start_command))
    
    # Help command
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from handlers.help import handle_help
        await handle_help(update, context)
    
    app.add_handler(CommandHandler("help", help_command))
    
    # Message handler for documents
    async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from handlers.upload import handle_document_upload
        await handle_document_upload(update, context)
    
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Message handler for text
    async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from handlers.chat import handle_user_message
        await handle_user_message(update, context)
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Callback query handler
    async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from handlers.callbacks import handle_callback
        await handle_callback(update, context)
    
    app.add_handler(CallbackQueryHandler(handle_callback_query))


def main():
    """Main function - start the bot."""
    try:
        logger.info("=" * 60)
        logger.info("🤖 Study Assistant Telegram Bot Starting...")
        logger.info("=" * 60)
        
        # Initialize database
        logger.info("📦 Initializing database...")
        init_db(Config.DATABASE_URL)
        logger.info("✅ Database initialized successfully")
        
        # Create persistence
        persistence = PicklePersistence(filepath="study_bot_persistence")
        
        # Create application
        app = Application.builder() \
            .token(Config.TELEGRAM_BOT_TOKEN) \
            .persistence(persistence) \
            .build()
        
        logger.info("📱 Telegram application created")
        
        # Setup handlers
        logger.info("⚙️  Setting up handlers...")
        setup_handlers(app)
        logger.info("✅ Handlers setup complete")
        
        # Start bot
        logger.info(f"🚀 Starting bot with polling (interval: {Config.POLLING_INTERVAL}s)...")
        logger.info(f"📊 AI Provider: {Config.AI_PROVIDER}")
        logger.info(f"💾 Database: {Config.DATABASE_TYPE}")
        logger.info(f"📁 Storage: {Config.STORAGE_TYPE}")
        logger.info(f"🧠 RAG Enabled: {Config.RAG_ENABLED}")
        
        app.run_polling(
            allowed_updates=["message", "callback_query"],
            poll_interval=Config.POLLING_INTERVAL,
        )
        
    except KeyboardInterrupt:
        logger.info("⏹️  Bot interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
