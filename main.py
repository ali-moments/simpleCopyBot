import asyncio
from telethon import TelegramClient, events
from secrets import APP_ID, APP_HASH, PREMIUM_APP_ID, PREMIUM_APP_HASH
import listener

reader = TelegramClient("reader_session", APP_ID, APP_HASH)
sender = TelegramClient("sender_session", PREMIUM_APP_ID, PREMIUM_APP_HASH)

is_active = True

message = """
DIAMOND
<tg-emoji emoji-id="5039816072253932764">💎</tg-emoji>
LONG_ARROW
<tg-emoji emoji-id="5449683594425410231">🔼</tg-emoji>
SHORT_ARROW
<tg-emoji emoji-id="5447183459602669338">🔽</tg-emoji>
ENTRY_EMOJI
<tg-emoji emoji-id="5443127283898405358">📥</tg-emoji>
LIGHTNING
<tg-emoji emoji-id="4956233646441760046">🌩</tg-emoji>
STOPLOSS_EMOJI
<tg-emoji emoji-id="4958621433509970793">🔖</tg-emoji>
WARNING
<tg-emoji emoji-id="5420323339723881652">⚠️</tg-emoji>
CROWN
<tg-emoji emoji-id="5843667185074969423">👑</tg-emoji>
"""


@sender.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply(message, parse_mode="html")


@sender.on(events.NewMessage(pattern='/on'))
async def on_handler(event):
    global is_active
    is_active = True
    await event.reply("✅ Bot is ON")


@sender.on(events.NewMessage(pattern='/off'))
async def off_handler(event):
    global is_active
    is_active = False
    await event.reply("🛑 Bot is OFF")


async def main():
    await reader.start()
    await sender.start()
    listener.register(reader, sender)
    print("✅ Both clients running")
    await reader.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
