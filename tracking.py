from pyrogram import filters
from pyrogram.types import Message

from client import bot
from database import add_user, add_chat


@bot.on_message(filters.private, group=1)
async def track_user(client, message: Message):
    if message.from_user:
        await add_user(message.from_user.id)


@bot.on_message(filters.group, group=1)
async def track_chat(client, message: Message):
    await add_chat(message.chat.id)
