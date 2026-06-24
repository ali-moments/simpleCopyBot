import re


def parse(text: str) -> dict | None:
    if not text:
        return None

    if "𝐒𝐈𝐆𝐍𝐀𝐋 𝐀𝐋𝐄𝐑𝐓" not in text:
        # print("Mahee: failed signal check")
        return None

    try:
        match = re.search(r"#([A-Z0-9]+/USDT)\s*\((\d+)x(LONG|SHORT)\)", text, re.IGNORECASE)
        if not match:
            return None

        symbol = match.group(1)
        # print(f"Mahee symbol: {symbol}")
        leverage = match.group(2) + "X"
        direction = match.group(3).upper()
        # print(f"Mahee leverage: {leverage}")

        entries = re.search(r"ENTRY:\s*([\d.]+)/([\d.]+)", text)
        # print(f"Mahee entries: {entries}")
        if not entries:
            return None
        entries = [float(entries.group(1)), float(entries.group(2))]

        targets_match = re.search(r"TARGETS:-?([\d./]+)", text)
        # print(f"Mahee targets: {targets_match}")
        if not targets_match:
            return None
        targets = [float(t) for t in targets_match.group(1).split("/")]

        sl = re.search(r"STOP LOSS:\s*([\d.]+)", text)
        # print(f"Mahee stop loss: {sl}")
        if not sl:
            return None
        sl = float(sl.group(1))

        return {
            "symbol": symbol,
            "direction": direction,
            "leverage": leverage,
            "entries": entries,
            "targets": targets,
            "stop_loss": sl,
            "source": "mahee",
        }

    except Exception:
        return None
