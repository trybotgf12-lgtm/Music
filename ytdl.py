import asyncio
import logging
import os
import shutil
import time
import yt_dlp

log = logging.getLogger("ytdl")

SECRET_COOKIES_PATH = "/etc/secrets/cookies.txt"
WRITABLE_COOKIES_PATH = "/tmp/cookies.txt"

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "geo_bypass": True,
    "nocheckcertificate": True,
}


def _setup_cookies():
    if os.path.exists(SECRET_COOKIES_PATH):
        shutil.copyfile(SECRET_COOKIES_PATH, WRITABLE_COOKIES_PATH)
        YDL_OPTS["cookiefile"] = WRITABLE_COOKIES_PATH
        log.info("Cookies loaded.")
    else:
        log.info("No cookies file found.")


def _extract(query: str) -> dict:
    _setup_cookies()
    last_error = None
    for attempt in range(3):
        try:
            with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(query, download=False)
                if "entries" in info:
                    info = info["entries"][0]
                return {
                    "title": info.get("title", "Unknown"),
                    "url": info.get("url"),
                    "webpage_url": info.get("webpage_url"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail"),
                }
        except Exception as e:
            last_error = e
            log.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(1.5)
    raise last_error


async def resolve_track(query: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract, query)
