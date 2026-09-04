from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream, Update
from pytgcalls.types.stream import StreamEnded

from client import bot, call_py
from song_queue import pop_next, clear_queue


@bot.on_message(filters.command("pause") & filters.group)
async def pause_cmd(client, message: Message):
    try:
        await call_py.pause(message.chat.id)
        await message.reply_text("⏸ Paused.")
    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


@bot.on_message(filters.command("resume") & filters.group)
async def resume_cmd(client, message: Message):
    try:
        await call_py.resume(message.chat.id)
        await message.reply_text("▶️ Resumed.")
    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


@bot.on_message(filters.command(["stop", "end"]) & filters.group)
async def stop_cmd(client, message: Message):
    chat_id = message.chat.id
    try:
        await call_py.leave_call(chat_id)
    except Exception:
        pass
    clear_queue(chat_id)
    await message.reply_text("⏹ Stopped and left the voice chat.")


@bot.on_message(filters.command("skip") & filters.group)
async def skip_cmd(client, message: Message):
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
@call_py.on_closed_voice_chat()
async def on_call_closed(client, chat_id):
    """Auto-rejoin and resume if the call gets unexpectedly closed."""
    from song_queue import current
    track = current(chat_id)
    if track:
        try:
            await call_py.play(chat_id, MediaStream(track["url"]))
        except Exception:
            pass
