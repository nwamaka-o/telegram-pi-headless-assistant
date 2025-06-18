"""
commands/media.py  capture photo using Pi Camera
"""
import asyncio
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

PHOTO_CMD = "libcamera-still -n -o {file} --width 1024 --height 768 --timeout 1000"


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("upload_photo")
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "snapshot.jpg"
        cmd = PHOTO_CMD.format(file=file_path)
        proc = await asyncio.create_subprocess_shell(cmd)
        await proc.communicate()

        if file_path.exists():
            await update.message.reply_photo(photo=open(file_path, "rb"))
        else:
            await update.message.reply_text("Failed to capture photo. Is the camera enabled?")
