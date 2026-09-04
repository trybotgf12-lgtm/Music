from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pytgcalls.types import MediaStream, Update
from pytgcalls.types.stream import StreamEnded

from client import bot, call_py
from song_queue import pop_next, clear_queue
from permissions import is_authorized
from database import approve_user


@bot.on_message(filters.command("pause") & filters.group)
async def pause_cmd(client, message: Message):
    if not await is_authorized(client, message.chat.id, message.from_user.id):
        await message.reply_text("⛔ Sirf group admin ya approved user hi ye kar sakta hai.")
        return
    try:
        await call_py.pause(message.chat.id)
        await message.reply_text("⏸ Paused.")
    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


@bot.on_message(filters.command("resume") & filters.group)
async def resume_cmd(client, message: Message):
    if not await is_authorized(client, message.chat.id, message.from_user.id):
        await message.reply_text("⛔ Sirf group admin ya approved user hi ye kar sakta hai.")
        return
    try:
        await call_py.resume(message.chat.id)
        await message.reply_text("▶️ Resumed.")
    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


@bot.on_message(filters.command(["stop", "end"]) & filters.group)
async def stop_cmd(client, message: Message):
    if not await is_authorized(client, message.chat.id, message.from_user.id):
        await message.reply_text("⛔ Sirf group admin ya approved user hi ye kar sakta hai.")
        return
    chat_id = message.chat.id
    try:
        await call_py.leave_call(chat_id)
    except Exception:
        pass
    clear_queue(chat_id)
    await message.reply_text("⏹ Stopped and left the voice chat.")


@bot.on_message(filters.command("skip") & filters.group)
async def skip_cmd(client, message: Message):
    if not await is_authorized(client, message.chat.id, message.from_user.id):
        await message.reply_text("⛔ Sirf group admin ya approved user hi ye kar sakta hai.")
        return
    chat_id = message.chat.id
    nxt = pop_next(chat_id)
    if not nxt:
        try:
            await call_py.leave_call(chat_id)
        except Exception:
            pass
        clear_queue(chat_id)
        await message.reply_text("⏭ Skipped. Queue is empty, left the voice chat.")
        return
    try:
        await call_py.play(chat_id, MediaStream(nxt["url"]))
        await message.reply_text(f"⏭ **Now playing:** {nxt['title']}")
    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


@bot.on_message(filters.command("musicapprove") & filters.group)
async def approve_cmd(client, message: Message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await message.reply_text("⛔ Sirf group admin/owner ye command use kar sakta hai.")
        return

    target_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            target_id = int(message.command[1])
        except ValueError:
            pass

    if not target_id:
        await message.reply_text(
            "Usage: kisi user ke message ko reply karke `/musicapprove` bhejo, "
            "ya `/musicapprove <user_id>`"
        )
        return

    await approve_user(message.chat.id, target_id)
    await message.reply_text(f"✅ User `{target_id}` ab is group me skip/stop/pause use kar sakta hai.")


@call_py.on_update()
async def on_stream_update(client, update: Update):
    if isinstance(update, StreamEnded):
        chat_id = update.chat_id
        nxt = pop_next(chat_id)
        if not nxt:
            try:
                await call_py.leave_call(chat_id)
            except Exception:
                pass
            return
        try:
            await call_py.play(chat_id, MediaStream(nxt["url"]))
        except Exception:
            clear_queue(chat_id)
