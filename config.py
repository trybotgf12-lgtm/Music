import os

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
PORT = int(os.environ.get("PORT", "8080"))
MONGO_URL = os.environ.get("MONGO_URL", "")

_sudo_raw = os.environ.get("SUDO_USERS", "")
SUDO_USERS = [int(x.strip()) for x in _sudo_raw.split(",") if x.strip()]
if OWNER_ID and OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)
