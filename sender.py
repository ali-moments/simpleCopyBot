from secrets import TARGET_CHANNEL

LONG_ARROW = '<tg-emoji emoji-id="5449683594425410231">🔼</tg-emoji>'
SHORT_ARROW = '<tg-emoji emoji-id="5447183459602669338">🔽</tg-emoji>'

def format_message(signal: dict) -> str:
    direction_arrow = LONG_ARROW if signal["direction"] == "LONG" else SHORT_ARROW

    if len(signal["entries"]) == 1:
        entry_text = f"EN: {signal['entries'][0]}~"
    else:
        entry_text = f"EN: {signal['entries'][0]} - {signal['entries'][1]}~"

    targets = signal["targets"]
    target_lines = ""
    for i, t in enumerate(targets, 1):
        target_lines += f"TARGET{i}⚡: {t}\n"

    leverage = signal["leverage"]

    text = (
        f'<b>💎 #{signal["symbol"]} | {signal["direction"]} {direction_arrow}</b>\n\n'
        f'<blockquote><b>ENTRY ورود</b></blockquote>\n'
        f'📥 {entry_text}\n\n'
        f'<blockquote><b>TARGETS حد سود</b></blockquote>\n'
        f'{target_lines}\n'
        f'<blockquote><b>STOPLOSS حد ضرر</b></blockquote>\n'
        f'🚩 SL: {signal["stop_loss"]}\n\n'
        f'⚠️ از 5 درصد مارجین و اهرم {leverage} استفاده کنید و بعد از تارگت اول سیو سود و ریسک فری کنید 💎\n\n'
        f'<blockquote>👑 @Royal_frx | رویال کریپتو</blockquote>'
    )

    return text


async def send(sender, signal: dict):
    text = format_message(signal)
    await sender.send_message(TARGET_CHANNEL, text, parse_mode="html")
