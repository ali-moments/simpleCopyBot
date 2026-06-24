from telethon import events
from parsers.monk import parse as monk_parse
from parsers.mahee import parse as mahee_parse
from parsers.gcr import parse as gcr_parse

CHANNELS = {
    # Test Channel for mock data
    # -1003971539633: gcr_parse,
    # Channels
    -1001581833855: monk_parse,
    -1003872504487: mahee_parse,
    -1001895114921: gcr_parse,
}


def register(reader, sender):
    @reader.on(events.NewMessage(chats=list(CHANNELS.keys())))
    async def handler(event):
        chat_id = event.chat_id
        parser = CHANNELS.get(chat_id)
        if not parser:
            return
        # print(repr(event.message.text))
        signal = parser(event.message.text.replace("**", ""))
        if signal:
            from sender import send
            await send(sender, signal)
