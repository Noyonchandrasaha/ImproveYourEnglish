import logging
import httpx
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from app.core.config import TELEGRAM_TOKEN, API_URL

logging.basicConfig(level=logging.INFO)

user_flags = {}

def set_awaiting_translation(user_id: int, awaiting: bool):
    user_flags[user_id] = {"awaiting_translation": awaiting}

def is_awaiting_translation(user_id: int):
    return user_flags.get(user_id, {}).get("awaiting_translation", False)

# Create a single global async HTTP client (reuse connections)
http_client = httpx.AsyncClient(timeout=10.0)

async def send_new_bangla_sentence(update: Update, user_id: int):
    try:
        resp = await http_client.get(f"{API_URL}/bangla_sentence", params={"user_id": user_id})
        resp.raise_for_status()
        sentence = resp.json()["sentence"]
    except Exception as e:
        logging.error(f"❌ Error fetching Bangla sentence: {e}")
        await update.message.reply_text("❌ Failed to fetch Bangla sentence from server.")
        return

    set_awaiting_translation(user_id, True)
    await update.message.reply_text(f"📝 Translate this Bangla sentence into English:\n\n{sentence}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start from user {update.effective_user.id}")
    user_id = update.effective_user.id
    await send_new_bangla_sentence(update, user_id)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    logging.info(f"User {user_id} sent message: {text}")

    if not is_awaiting_translation(user_id):
        await send_new_bangla_sentence(update, user_id)
        return

    payload = {
        "user_id": user_id,
        "user_translation": text,
    }

    try:
        resp = await http_client.post(f"{API_URL}/correction", json=payload)
        resp.raise_for_status()
        correction = resp.json()["correction"]
    except Exception as e:
        logging.error(f"❌ Error getting correction: {e}")
        await update.message.reply_text("❌ Failed to get correction from server.")
        return

    set_awaiting_translation(user_id, False)
    await update.message.reply_text("✅ Checking your translation...")
    await update.message.reply_text(correction)

    await send_new_bangla_sentence(update, user_id)

def run_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("🤖 Telegram bot running...")
    application.run_polling()

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(run_bot())
    except Exception as e:
        logging.error(f"Bot stopped with exception: {e}")
    finally:
        # Close HTTP client gracefully
        asyncio.run(http_client.aclose())
