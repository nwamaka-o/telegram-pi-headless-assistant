"""
Example periodic notifier  send the Pi's IP every hour.
Call from bot.py if you want background jobs.
"""
import asyncio

from telegram.ext import Application


async def hourly_ip_report(application: Application):
    while True:
        bot = application.bot
        public_ip = (await (await asyncio.create_subprocess_shell(
            "curl -s https://ifconfig.me", stdout=asyncio.subprocess.PIPE
        )).communicate())[0].decode().strip()

        for chat_id in application.bot_data.get("ALLOWED_IDS", []):
            await bot.send_message(chat_id=chat_id, text=f"Hourly IP check: {public_ip}")
        await asyncio.sleep(3600)
