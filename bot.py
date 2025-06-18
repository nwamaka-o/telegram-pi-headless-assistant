#!/usr/bin/env python3
#bot.py Telegram Headless Assistant for Raspberry Pi

import asyncio
import functools
import logging
import os
from pathlib import Path
from typing import Callable, Awaitable

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

# --------------------------------------------------------------------------- #
#  Environment & Globals
# --------------------------------------------------------------------------- #
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_IDS = {int(x) for x in os.getenv("ALLOWED_IDS", "").split(",") if x}

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("telegram_pi_headless")

# --------------------------------------------------------------------------- #
#  Decorator to restrict commands to whitelisted chats
# --------------------------------------------------------------------------- #
def allowed_only(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        if user_id not in ALLOWED_IDS and chat_id not in ALLOWED_IDS:
            logger.warning("Unauthorized access from %s", user_id)
            return  # silently ignore
        return await func(update, context)

    return wrapper

# --------------------------------------------------------------------------- #
#  Command Handlers (delegated to commands/ modules)
# --------------------------------------------------------------------------- #
from commands import system as sys_cmd       # noqa: E402
from commands import admin as admin_cmd      # noqa: E402
from commands import media as media_cmd      # noqa: E402


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing  set in .env")

    application: Application = ApplicationBuilder().token(BOT_TOKEN).build()

    # System information
    application.add_handler(CommandHandler("ip", allowed_only(S.ip)))
    application.add_handler(CommandHandler("uptime", allowed_only(sys_cmd.uptime)))
    application.add_handler(CommandHandler("temp", allowed_only(sys_cmd.cpu_temp)))
    application.add_handler(CommandHandler("disk", allowed_only(sys_cmd.disk)))

    # Media
    application.add_handler(CommandHandler("photo", allowed_only(media_cmd.photo)))

    # Admin
    application.add_handler(CommandHandler("reboot", allowed_only(admin_cmd.reboot)))
    application.add_handler(CommandHandler("shutdown", allowed_only(admin_cmd.shutdown)))

    # Help / start message
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(
            "?? <b>Telegram Headless Assistant</b>\n"
            "Send /ip, /uptime, /temp, /disk, /photo, /reboot, /shutdown"
        )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))

    # Run the bot (long-polling; for webhooks, see docs)
    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
