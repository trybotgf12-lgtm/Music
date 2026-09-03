from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream, Update
from pytgcalls.types.stream import StreamEnded

from bot.client import call_py
from bot.helpers.queue import pop_next, current, clear_queue, get_queue


@Client.on_message(filters.command("pause") & filters.group)
async def pause_cmd(client: Client, message: Message):
    try:
        await call_py.pause(message.chat.id)
        await message.reply_text("⏸ Paused.")
    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


@Client.on_message(filters.command("resume") & filters.group)
async def resume_cmd(client: Client, message: Message):
    try:
        await call_py.resume(message.chat.id)
        await message.reply_text("▶️ Resumed.")
    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


@Client.on_message(filters.command(["stop", "end"]) & filters.group)
async def stop_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        await call_py.leave_call(chat_id)
    except Exception:
        pass
    clear_queue(chat_id)
    await message.reply_text("⏹ Stopped and left the voice chat.")


@Client.on_message(filters.command("skip") & filters.group)
async def skip_cmd(client: Client, message: Message):
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


@call_py.on_update()
async def on_stream_update(client, update: Update):
    """Auto-advance the queue when a track finishes."""
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
