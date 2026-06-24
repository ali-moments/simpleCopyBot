from secrets import TARGET_CHANNEL

DIAMOND = '<tg-emoji emoji-id="5039816072253932764">💎</tg-emoji>'
LONG_ARROW = '<tg-emoji emoji-id="5449683594425410231">🔼</tg-emoji>'
SHORT_ARROW = '<tg-emoji emoji-id="5447183459602669338">🔽</tg-emoji>'
ENTRY_EMOJI = '<tg-emoji emoji-id="5443127283898405358">📥</tg-emoji>'
LIGHTNING = '<tg-emoji emoji-id="4956233646441760046">🌩</tg-emoji>'
STOPLOSS_EMOJI = '<tg-emoji emoji-id="4958621433509970793">🔖</tg-emoji>'
WARNING = '<tg-emoji emoji-id="5420323339723881652">⚠️</tg-emoji>'
CROWN = '<tg-emoji emoji-id="5843667185074969423">👑</tg-emoji>'


def format_message(signal: dict) -> str:
    direction_arrow = LONG_ARROW if signal["direction"] == "LONG" else SHORT_ARROW

    if len(signal["entries"]) == 1:
        entry_text = f"{signal['entries'][0]}~"
    else:
        entry_text = f"{signal['entries'][0]} - {signal['entries'][1]}~"

    targets = signal["targets"]
    target_lines = ""
    for i, t in enumerate(targets, 1):
        target_lines += f"<b>TARGET{i}{LIGHTNING}: {t}</b>\n"

    leverage = signal["leverage"]

    text = (
        f'<b><b>{DIAMOND} #{signal["symbol"]} | {signal["direction"]} {direction_arrow}</b>\n\n'
        f'<blockquote><b>ENTRY ورود</b></blockquote>\n'
        f'<b>{ENTRY_EMOJI}EN: {entry_text}</b>\n\n'
        f'<blockquote><b>TARGETS حد سود</b></blockquote>'
        f'{target_lines}\n'
        f'<blockquote><b>STOPLOSS حد ضرر</b></blockquote>\n'
        f'<b>{STOPLOSS_EMOJI}SL: {signal["stop_loss"]}</b>\n\n'
        f'<b>{WARNING} از 5 درصد مارجین و اهرم {leverage} استفاده کنید و بعد از تارگت اول سیو سود و ریسک فری کنید {DIAMOND}</b>\n\n'
        f'<blockquote>{CROWN} <b>@Royal_frx</b> | رویال کریپتو</blockquote></b>'
    )

    return text


async def send(sender, signal: dict):
    text = format_message(signal)
    # await sender.send_message("me", text, parse_mode="html")
    await sender.send_message(TARGET_CHANNEL, text, parse_mode="html")
