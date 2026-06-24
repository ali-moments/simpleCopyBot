import re


def parse(text: str) -> dict | None:
    if not text:
        return None

    if "Coin #" not in text:
        # print("GCR: failed signal check")
        return None

    try:
        symbol = re.search(r"#([A-Z0-9]+/USDT)", text)
        # print(f"GCR symbol: {symbol}")
        if not symbol:
            return None
        symbol = symbol.group(1)

        direction = re.search(r"Position:\s*(LONG|SHORT)", text, re.IGNORECASE)
        # print(f"GCR direction: {direction}")
        if not direction:
            return None
        direction = direction.group(1).upper()

        leverage = re.search(r"Leverage:[\s\xa0]+Cross\s*(\d+)×\s*To\s*(\d+)×", text)
        leverage = f"{leverage.group(1)}X-{leverage.group(2)}X" if leverage else "10X-50X"

        entries = re.search(r"Entries:\s*([\d.]+)\s*-\s*([\d.]+)", text)
        # print(f"GCR entries: {entries}")
        if not entries:
            return None
        entries = [float(entries.group(1)), float(entries.group(2))]

        targets = re.search(r"Targets:.*?([\d.]+),\s*([\d.]+),\s*([\d.]+)", text)
        # print(f"GCR targets: {targets}")
        if not targets:
            return None
        targets = [float(targets.group(i)) for i in range(1, 4)]

        sl = re.search(r"Stop Loss:\s*([\d.]+)", text)
        # print(f"GCR sl: {sl}")
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
            "source": "gcr",
        }

    except Exception:
        return None
