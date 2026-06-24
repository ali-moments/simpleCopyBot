import os
from typing import Final

APP_ID: Final = int(os.environ["APP_ID"])
APP_HASH: Final = os.environ["APP_HASH"]
PREMIUM_APP_ID: Final = int(os.environ["PREMIUM_APP_ID"])
PREMIUM_APP_HASH: Final = os.environ["PREMIUM_APP_HASH"]
TARGET_CHANNEL: Final = int(os.environ["TARGET_CHANNEL"])
