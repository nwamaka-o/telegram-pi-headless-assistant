"""
commands/admin.py  reboot & shutdown (requires sudo privileges)
"""
import asyncio
import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? Rebooting in 5 seconds")
    await asyncio.sleep(5)
    proc = await asyncio.create_subprocess_shell("sudo reboot")
    await proc.communicate()


async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("? Shutting down in 5 seconds")
    await asyncio.sleep(5)
    proc = await asyncio.create_subprocess_shell("sudo shutdown now")
    await proc.communicate()
