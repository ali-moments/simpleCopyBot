# 🤖 CopyBot

A Telegram client that monitors crypto signal channels, parses incoming signals, and forwards them to your channel in a clean, formatted template — with premium emoji support.

---

## Architecture

```
reader (Telethon user client)
    └── listens to 3 source channels
    └── routes messages to channel-specific parsers
    └── passes parsed signal dict to sender

sender (Telethon premium user client)
    └── formats signal into template
    └── sends to your target channel with premium emojis
```

Two independent Telethon clients run in the same async event loop:
- **reader** — your regular account that is a member of the source channels
- **sender** — a premium account that posts formatted signals to your channel

---

## Supported Source Channels

| Channel | Parser | Entries | Targets |
|---|---|---|---|
| CRYPTO MONK PREMIUM | `parsers/monk.py` | 1 | 5 |
| Mahee VIP | `parsers/mahee.py` | 2 | 3 |
| GCR VVIP | `parsers/gcr.py` | 2 | 3 |

---

## Project Structure

```
copyBot/
├── main.py           # boots both clients, registers handlers
├── listener.py       # routes incoming messages to parsers
├── sender.py         # formats and sends signals to target channel
├── secrets.py        # loads credentials from environment variables
├── parsers/
│   ├── __init__.py
│   ├── monk.py
│   ├── mahee.py
│   └── gcr.py
├── Dockerfile
├── docker-compose.yml
├── .env.example      # template for credentials
└── .gitignore
```

---

## Requirements

- Docker + Docker Compose
- A Telegram account (reader) that is a member of the source channels
- A Telegram **premium** account (sender) that is an admin of your target channel
- API credentials from [my.telegram.org](https://my.telegram.org) for both accounts

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/copyBot.git
cd copyBot
```

### 2. Create your `.env` file

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
APP_ID=12345678
APP_HASH=your_reader_account_app_hash
PREMIUM_APP_ID=87654321
PREMIUM_APP_HASH=your_premium_account_app_hash
TARGET_CHANNEL=-1001234567890
PYTHONUNBUFFERED=1
```

#### How to get API credentials

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Log in with the account's phone number
3. Click **API development tools**
4. Fill in any app name and select **Desktop** as platform
5. Copy `api_id` and `api_hash`

Repeat for both accounts (reader and sender).

#### How to get your channel ID

Forward any message from your channel to [@userinfobot](https://t.me/userinfobot) — it will return the channel ID (negative number starting with `-100`).

---

### 3. Authenticate sessions

On first run, Telethon needs to authenticate both accounts interactively. Run:

```bash
docker compose run --rm copybot uv run main.py
```

- Enter the **reader account** phone number and the code Telegram sends you
- Enter the **sender account** phone number and the code Telegram sends you

Session files (`reader_session.session`, `sender_session.session`) will be created in the project directory. Press `Ctrl+C` after both sessions are authenticated.

> ⚠️ Session files are mounted as volumes and never baked into the Docker image. Keep them safe and never commit them.

---

### 4. Run

```bash
docker compose up -d
```

### 5. View logs

```bash
docker compose logs -f
```

### 6. Stop

```bash
docker compose down
```

---

## Signal Format

Each parsed signal is passed as a dict:

```python
{
    "symbol": "SUI/USDT",
    "direction": "LONG",        # or SHORT
    "leverage": "20X",
    "entries": [0.7191],        # 1 or 2 prices
    "targets": [0.71, 0.70],    # 3 or 5 prices
    "stop_loss": 0.7302,
    "source": "monk"            # monk | mahee | gcr
}
```

---

## Adding a New Channel

1. Add the channel ID and its parser to `listener.py`:
```python
CHANNELS = {
    -1001234567890: new_parse,
}
```

2. Create `parsers/new_channel.py` with a `parse(text: str) -> dict | None` function
3. Return `None` for non-signal messages, return the signal dict for valid signals

---

## Notes

- Premium emojis in the output template require the **sender account to be a Telegram Premium subscriber** and an **admin of the target channel**
- Session files persist across container restarts via Docker volumes — you only need to authenticate once
- The bot handles both plain-text and premium-emoji formatted messages from source channels (strips markdown artifacts automatically)