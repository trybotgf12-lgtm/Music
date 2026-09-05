from pyrogram import filters
from pyrogram.types import Message

from client import bot

START_TEXT = """👋 **Hey, I'm a Telegram Music Bot!**

Add me to a group, promote me as admin, and use:

• `/play <song name or YouTube link>` — play in voice chat
• `/pause` — pause playback
• `/resume` — resume playback
• `/skip` — skip current song
• `/queue` — show queue
• `/stop` — stop and leave voice chat
"""


@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    print(f"START RECEIVED: {message.from_user.id}", flush=True)
    await message.reply_text(START_TEXT)


@bot.on_message(filters.command("start") & filters.group)
async def start_group_cmd(client, message: Message):
    print(f"GROUP START RECEIVED: {message.chat.id}", flush=True)
    await message.reply_text(
        "I'm alive! Use /play <song name> to start playing music."
    )


@bot.on_message(filters.text)
async def debug_message(client, message: Message):
    print(
        f"MESSAGE RECEIVED: chat={message.chat.id} text={message.text!r}",
        flush=True
    )
