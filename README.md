# Telegram Headless Assistant for Raspberry Pi

Remotely control your Raspberry Pi via Telegram bot messages — no monitor, keyboard, or open SSH ports required.

## 🔍 Project Overview

The **Telegram Headless Assistant** is a lightweight Python-based bot designed to manage a Raspberry Pi entirely over Telegram. It provides quick system health checks, remote administrative actions, and camera access, all from the convenience of your Telegram app.

Key capabilities:

- 📡 Get public and local IP addresses
- ⏱️ Check uptime and CPU temperature
- 💾 Monitor disk usage
- 📷 Capture and receive photos from the Pi camera
- 🔁 Reboot or shutdown the Pi securely

## ⚙️ Features

- **Text-based remote control** from Telegram
- **System commands**: `/ip`, `/uptime`, `/temp`, `/disk`
- **Maintenance commands**: `/reboot`, `/shutdown` (with sudoers protection)
- **Camera support**: `/photo` for instant snapshots
- **Security-first design**: API token in `.env`, command whitelisting
- **Runs as a `systemd` service** for auto-start on boot
- **Supports Wi-Fi, Ethernet, or LTE connections**

## 📐 Architecture

```

Telegram Cloud ↔️ Bot API ↔️ bot.py ↔️ Raspberry Pi OS & GPIO

````

- **Stateless command processing** via long polling or webhook
- **Modular command handlers** mapped to shell/Python functions
- **Secure, async architecture** using `python-telegram-bot` 23.x

## 🧰 Tech Stack

- 🐍 Python 3.12
- 📦 `python-telegram-bot`, `gpiozero`, `psutil`, `python-dotenv`
- 📱 Telegram Bot API
- 📷 Raspberry Pi (Zero W, 4B, 5) with RPi OS Bookworm

## 🚀 Getting Started

### 1. 🧪 Requirements

- Raspberry Pi (any model with network support)
- Raspberry Pi OS (Bookworm recommended)
- Telegram account and bot token

### 2. 🛠️ Installation

```bash
sudo apt update && sudo apt install python3-pip
pip install -r requirements.txt
````

> Add your bot token and allowed user IDs in `.env` (see below).

### 3. 🔐 Configure `.env`

Create a `.env` file in the root directory:

```env
BOT_TOKEN=your_telegram_bot_token
ALLOWED_IDS=123456789,987654321
```

* `BOT_TOKEN`: Provided by [@BotFather](https://t.me/botfather)
* `ALLOWED_IDS`: Comma-separated list of Telegram user IDs allowed to control the bot

### 4. 🧪 Run the Bot

```bash
python3 bot.py
```

Or set it up as a `systemd` service to run on boot (see `service-example.service` if included).

## 📎 Key Bot Commands

| Command     | Description                       |
| ----------- | --------------------------------- |
| `/ip`       | Shows public and local IP         |
| `/uptime`   | Returns system uptime             |
| `/temp`     | Shows CPU temperature (°C)        |
| `/disk`     | Displays disk usage               |
| `/photo`    | Takes and sends a Pi camera photo |
| `/reboot`   | Reboots the Pi (requires sudo)    |
| `/shutdown` | Shuts down the Pi (requires sudo) |

## 🔐 Security Considerations

* `.env` is excluded via `.gitignore` — **never commit your token**
* Only whitelisted chat IDs can issue commands
* `sudo` permissions limited to safe commands via `/etc/sudoers.d/pi-telegram-bot`:

```bash
pi ALL=(ALL) NOPASSWD: /sbin/reboot, /sbin/shutdown
```

* Optional: Run bot within a VPN (e.g., WireGuard) for extra protection

## 🔍 Logs & Monitoring

* Logs are written to `journald` if run under `systemd`
* Responds in <1s over Wi-Fi and LTE
* Uptime tested for over 30 days

## 📈 Use Cases

* Remote control in IoT or sensor deployments
* Monitor headless Pi devices without SSH
* Instant recovery or reboot for field devices
* Alert delivery via Telegram (watchdog or sensors)

## 🧭 Future Enhancements

* Voice command recognition via voice notes
* Self-update/OTA functionality
* MQTT integration for Home Assistant
* Interactive inline keyboards and menus

## 📚 References

* [python-telegram-bot docs](https://docs.python-telegram-bot.org/)
* [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
* Project Repo: [https://github.com/nwamaka-o/telegram-pi-headless-assistant](https://github.com/nwamaka-o/telegram-pi-headless-assistant)


