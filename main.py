import asyncio
from telethon import TelegramClient
from secrets import APP_ID, APP_HASH, BOT_TOKEN
import listener

reader = TelegramClient("reader_session", APP_ID, APP_HASH)
sender = TelegramClient("sender_session", APP_ID, APP_HASH)


async def main():
    await reader.start()
    await sender.start(bot_token=BOT_TOKEN)
    listener.register(reader, sender)
    print("✅ Both clients running")
    await reader.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
