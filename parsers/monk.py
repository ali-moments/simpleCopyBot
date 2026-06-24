import re


def parse(text: str) -> dict | None:
    if not text:
        return None

    # check if signal
    if not re.search(r"#(LONG|SHORT)", text, re.IGNORECASE):
        # print("Monk: failed signal check")
        return None

    try:
        direction = "LONG" if "#LONG" in text.upper() else "SHORT"
        # print(f"Monk direction: {direction}")

        symbol = re.search(r"#([A-Z0-9]+/USDT)", text)
        # print(f"Monk symbol: {symbol}")
        if not symbol:
            return None
        symbol = symbol.group(1)

        entry = re.search(r"BUY\s*:\s*\n?1\)\s*([\d.]+)", text)
        # print(f"Monk entry: {entry}")
        if not entry:
            return None
        entry = float(entry.group(1))

        targets = re.findall(r"[\U0001F7E5\U0001F7E9]\s*([\d.]+)", text)
        # print(f"Monk targets: {targets}")
        targets = [float(t) for t in targets]

        sl = re.search(r"SL\s*:\s*([\d.]+)", text)
        # print(f"Monk SL: {sl}")
        if not sl:
            return None
        sl = float(sl.group(1))

        leverage = re.search(r"LEV\s*:\s*(\d+X)", text)
        leverage = leverage.group(1) if leverage else "20X"

        return {
            "symbol": symbol,
            "direction": direction,
            "leverage": leverage,
            "entries": [entry],
            "targets": targets,
            "stop_loss": sl,
            "source": "monk",
        }

    except Exception:
        return None
