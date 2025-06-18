"""
commands/system.py  gather system info
"""
import asyncio
import platform
import socket
import subprocess
from datetime import timedelta

import psutil
from telegram import Update
from telegram.ext import ContextTypes


async def _get_public_ip() -> str:
    """Fetch public IP via an external service (non-blocking)."""
    proc = await asyncio.create_subprocess_shell(
        "curl -s https://ifconfig.me",
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    out, _ = await proc.communicate()
    return out.decode().strip() or "N/A"


async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    public_ip = await _get_public_ip()
    await update.message.reply_text(
        f"?? Local IP: <code>{local_ip}</code>\n?? Public IP: <code>{public_ip}</code>",
        parse_mode="HTML",
    )


async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    boot_ts = psutil.boot_time()
    uptime_td = timedelta(seconds=int(psutil.time.time() - boot_ts))
    await update.message.reply_text(f"? Uptime: <b>{uptime_td}</b>", parse_mode="HTML")


async def cpu_temp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temp_c = psutil.sensors_temperatures().get("cpu-thermal") or \
        psutil.sensors_temperatures().get("cpu_thermal")
    if temp_c:
        temp_c = temp_c[0].current
        await update.message.reply_text(f"?? CPU temperature: <b>{temp_c:.1f} C</b>", parse_mode="HTML")
    else:
        await update.message.reply_text("Temperature sensor not available.")


async def disk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usage = psutil.disk_usage("/")
    await update.message.reply_text(
        f"?? Disk: {usage.used // (1024**3)} GiB used / "
        f"{usage.total // (1024**3)} GiB total "
        f"({usage.percent} %)"
    )
