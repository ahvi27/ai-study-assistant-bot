"""
Flashcard Handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.constants import ChatAction
from database import get_session, UserDB, DocumentDB, FlashcardDB
from services import FlashcardService
from utils.logger import logger
from keyboards import get_back_keyboard, get_flashcard_action_keyboard


async def flashcards_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /flashcards command"""
    try:
        chat_id = update.effective_chat.id

        message = """🎴 *Flashcard System*

Create and study flashcards from your notes.

Options:
• Create new flashcards
• Review existing flashcards
• View statistics

What would you like to do?"""

        keyboard = [
            [InlineKeyboardButton("📝 Create Flashcards", callback_data="fc_create")],
            [InlineKeyboardButton("🔄 Review Flashcards", callback_data="fc_review")],
            [InlineKeyboardButton("📊 Statistics", callback_data="fc_stats")],
            [InlineKeyboardButton("« Back", callback_data="back_to_main")],
        ]

        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        logger.info(f"User {update.effective_user.id} accessed flashcards")

    except Exception as e:
        logger.error(f"Error in flashcards command: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ An error occurred.",
        )


async def flashcard_create_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle flashcard creation"""
    try:
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        chat_id = query.message.chat_id

        # Show processing
        await query.edit_message_text(text="⏳ Generating flashcards...")
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

        session = get_session()
        user = UserDB.get_user(session, user_id)

        if not user:
            session.close()
            await query.edit_message_text("❌ User not found.")
            return

        documents = DocumentDB.get_user_documents(session, user.id)

        if not documents or not documents[0].text_content:
            session.close()
            await query.edit_message_text(
                "❌ No documents uploaded yet. Please upload a document first.",
                reply_markup=get_back_keyboard(),
            )
            return

        content = documents[0].text_content[:3000]  # Limit content

        # Generate flashcards
        flashcard_service = FlashcardService()
        flashcards = flashcard_service.generate_flashcards(
            content,
            num_cards=10,
            difficulty="medium",
        )

        if not flashcards:
            session.close()
            await query.edit_message_text(
                "❌ Could not generate flashcards. Please try again.",
                reply_markup=get_back_keyboard(),
            )
            return

        # Save flashcards to database
        for fc in flashcards:
            FlashcardDB.create_flashcard(
                session,
                user_id=user.id,
                question=fc.get("question", ""),
                answer=fc.get("answer", ""),
                difficulty=fc.get("difficulty", "medium"),
                document_id=documents[0].id if documents else None,
            )

        session.close()

        # Store in context
        context.user_data["current_flashcards"] = flashcards
        context.user_data["fc_index"] = 0
        context.user_data["fc_show_answer"] = False

        # Display first flashcard
        await display_flashcard(query.message, context, flashcards[0], 1, len(flashcards))

        logger.info(f"Created {len(flashcards)} flashcards for user {user_id}")

    except Exception as e:
        logger.error(f"Error creating flashcards: {e}")
        await query.answer(text="❌ Error creating flashcards", show_alert=True)


async def display_flashcard(message, context: ContextTypes.DEFAULT_TYPE, card: dict, current: int, total: int) -> None:
    """Display a flashcard"""
    try:
        show_answer = context.user_data.get("fc_show_answer", False)

        text = f"""*Flashcard {current}/{total}*

{card.get('question', '')}
"""

        if show_answer:
            text += f"\n*Answer:*\n{card.get('answer', '')}"

        keyboard = [
            [
                InlineKeyboardButton("◀️ Back", callback_data="fc_previous"),
                InlineKeyboardButton("Show Answer" if not show_answer else "Hide Answer",
                                     callback_data="fc_toggle_answer"),
                InlineKeyboardButton("Next ▶️", callback_data="fc_next"),
            ],
            [
                InlineKeyboardButton("✅ Got it", callback_data="fc_correct"),
                InlineKeyboardButton("❌ Review", callback_data="fc_incorrect"),
            ],
            [InlineKeyboardButton("« Back", callback_data="back_to_main")],
        ]

        await message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    except Exception as e:
        logger.error(f"Error displaying flashcard: {e}")


async def flashcard_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle flashcard navigation"""
    try:
        query = update.callback_query
        await query.answer()

        callback_data = query.data
        flashcards = context.user_data.get("current_flashcards", [])
        current_index = context.user_data.get("fc_index", 0)

        if callback_data == "fc_next":
            current_index = min(current_index + 1, len(flashcards) - 1)
            context.user_data["fc_show_answer"] = False
        elif callback_data == "fc_previous":
            current_index = max(current_index - 1, 0)
            context.user_data["fc_show_answer"] = False
        elif callback_data == "fc_toggle_answer":
            context.user_data["fc_show_answer"] = not context.user_data.get("fc_show_answer", False)

        context.user_data["fc_index"] = current_index

        if flashcards:
            await display_flashcard(
                query.message,
                context,
                flashcards[current_index],
                current_index + 1,
                len(flashcards),
            )

    except Exception as e:
        logger.error(f"Error in flashcard navigation: {e}")
        await query.answer(text="❌ Error", show_alert=True)


async def flashcard_review_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle flashcard review feedback"""
    try:
        query = update.callback_query
        await query.answer()

        callback_data = query.data
        flashcards = context.user_data.get("current_flashcards", [])
        current_index = context.user_data.get("fc_index", 0)

        if current_index < len(flashcards):
            correct = callback_data == "fc_correct"
            # In real implementation, would save to database
            logger.info(f"Flashcard review: {'correct' if correct else 'incorrect'}")

        # Move to next
        current_index = min(current_index + 1, len(flashcards) - 1)
        context.user_data["fc_index"] = current_index
        context.user_data["fc_show_answer"] = False

        if current_index < len(flashcards):
            await display_flashcard(
                query.message,
                context,
                flashcards[current_index],
                current_index + 1,
                len(flashcards),
            )
        else:
            await query.edit_message_text(
                "✅ Flashcard review completed! Great job! 🎉",
                reply_markup=get_back_keyboard(),
            )

    except Exception as e:
        logger.error(f"Error in flashcard review: {e}")
        await query.answer(text="❌ Error", show_alert=True)


def get_flashcard_handlers():
    """Get flashcard handlers"""
    return [
        CommandHandler("flashcards", flashcards_command),
        CallbackQueryHandler(flashcard_create_callback, pattern="^fc_create$"),
        CallbackQueryHandler(flashcard_navigation, pattern="^fc_(next|previous|toggle_answer)$"),
        CallbackQueryHandler(flashcard_review_callback, pattern="^fc_(correct|incorrect)$"),
    ]
