import asyncio
import logging

from aiohttp import web

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, PORT
from client import bot, assistant, call_py
import start
import play
import controls

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")


async def health(_):
    return web.Response(text="Music bot is alive.")


async def run_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    log.info(f"Health server listening on port {PORT}")


async def main():
    missing = [
        name
        for name, val in [
            ("API_ID", API_ID),
            ("API_HASH", API_HASH),
            ("BOT_TOKEN", BOT_TOKEN),
            ("SESSION_STRING", SESSION_STRING),
        ]
        if not val
    ]
    if missing:
        raise SystemExit(f"Missing required env vars: {', '.join(missing)}.")

    await run_web_server()
    await bot.start()
    log.info("Bot client started.")
    await assistant.start()
    log.info("Assistant client started.")
    await call_py.start()
    log.info("PyTgCalls started. Bot is ready.")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
