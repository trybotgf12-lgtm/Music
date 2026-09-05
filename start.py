from pyrogram import Client, filters
from pyrogram.types import Message

START_TEXT = """👋 **Hey, I'm a Telegram Music Bot!**

Add me to a group, promote me as admin, and use:
• `/play <song name or YouTube link>` — play in voice chat
• `/pause` — pause playback
• `/resume` — resume playback
• `/skip` — skip current song
• `/queue` — show queue
• `/stop` — stop and leave voice chat

Made for group voice chats. Assistant account joins the VC to stream audio.
"""


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    await message.reply_text(START_TEXT)


@Client.on_message(filters.command("start") & filters.group)
async def start_group_cmd(client: Client, message: Message):
    await message.reply_text("I'm alive! Use /play <song name> to start playing music.")
