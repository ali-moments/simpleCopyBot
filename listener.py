from collections import deque
from telethon import events
from parsers.monk import parse as monk_parse
from parsers.mahee import parse as mahee_parse
from parsers.gcr import parse as gcr_parse
import main

CHANNELS = {
    # Test Channel for mock data
    # -1003971539633: gcr_parse,
    # Channels
    -1001581833855: monk_parse,
    -1003872504487: mahee_parse,
    -1001895114921: gcr_parse,
}

seen_ids = deque(maxlen=100)


def register(reader, sender):
    @reader.on(events.NewMessage(chats=list(CHANNELS.keys())))
    async def handler(event):
        if not main.is_active:
            return
        msg_id = (event.chat_id, event.message.id)
        if msg_id in seen_ids:
            return
        seen_ids.append(msg_id)

        chat_id = event.chat_id
        parser = CHANNELS.get(chat_id)
        if not parser:
            return

        # print(repr(event.message.text))
        signal = parser(event.message.text.replace("**", ""))
        if signal:
            from sender import send
            await send(sender, signal)
