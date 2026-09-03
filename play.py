from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream
from pytgcalls.exceptions import NoActiveGroupCall

from client import bot, call_py
from ytdl import resolve_track
from song_queue import add_to_queue, get_queue, clear_queue


@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/play <song name or YouTube link>`")
        return

    query = message.text.split(None, 1)[1]
    status = await message.reply_text(f"🔎 Searching: **{query}** ...")

    try:
        track = await resolve_track(query)
    except Exception as e:
        await status.edit_text(f"❌ Couldn't find that track.\n`{e}`")
        return

    chat_id = message.chat.id
    position = add_to_queue(chat_id, track)

    if position == 1:
        try:
            await call_py.play(chat_id, MediaStream(track["url"]))
            await status.edit_text(f"▶️ **Now playing:** {track['title']}")
        except NoActiveGroupCall:
            await status.edit_text(
                "❌ No active voice chat found. Start a voice chat in this group first."
            )
            clear_queue(chat_id)
        except Exception as e:
            await status.edit_text(f"❌ Failed to play: `{e}`")
            clear_queue(chat_id)
    else:
        await status.edit_text(f"➕ **Added to queue (#{position}):** {track['title']}")


@bot.on_message(filters.command(["queue", "q"]) & filters.group)
async def queue_cmd(client, message: Message):
    q = get_queue(message.chat.id)
    if not q:
        await message.reply_text("Queue is empty.")
        return
    lines = [f"{i+1}. {t['title']}" for i, t in enumerate(q)]
    await message.reply_text("🎶 **Queue:**\n" + "\n".join(lines))
