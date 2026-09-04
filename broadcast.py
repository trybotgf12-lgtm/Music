import asyncio

from pyrogram import filters
from pyrogram.types import Message

from client import bot
from config import SUDO_USERS
from database import get_all_users, get_all_chats


@bot.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast_cmd(client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Kisi message (text/photo) ko reply karke `/broadcast` bhejo.")
        return

    users = await get_all_users()
    chats = await get_all_chats()
    targets = users + chats

    status = await message.reply_text(f"📢 Broadcasting to {len(targets)} chats...")

    sent, failed = 0, 0
    for target_id in targets:
        try:
            await message.reply_to_message.copy(target_id)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)

    await status.edit_text(f"✅ Broadcast done. Sent: {sent}, Failed: {failed}")
