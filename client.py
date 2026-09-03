from pyrogram import Client
from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

# Bot account -> receives commands
bot = Client(
    name="music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="bot/plugins"),
)

# Assistant (userbot) account -> actually joins the voice chat and streams audio.
# Telegram bots cannot join voice chats themselves, so a normal user session is
# required. Generate SESSION_STRING using generate_session.py.
assistant = Client(
    name="assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

call_py = PyTgCalls(assistant)
