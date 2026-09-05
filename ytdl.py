import asyncio
import logging
import os
import shutil
import time
import yt_dlp

log = logging.getLogger("ytdl")

SECRET_COOKIES_PATH = "/etc/secrets/cookies.txt"
WRITABLE_COOKIES_PATH = "/tmp/cookies.txt"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "http_headers": {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
    },
    # PO Token provider (bgutil, Node.js) is auto-detected once installed —
    # no extra extractor_args needed, it registers itself automatically.
}


def _setup_cookies():
    if os.path.exists(SECRET_COOKIES_PATH):
        shutil.copyfile(SECRET_COOKIES_PATH, WRITABLE_COOKIES_PATH)
        YDL_OPTS["cookiefile"] = WRITABLE_COOKIES_PATH
        log.info("Cookies loaded.")
    else:
        log.info("No cookies file found — proceeding without cookies.")


def _extract(query: str) -> dict:
    _setup_cookies()
    last_error = None
    for attempt in range(4):
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
            log.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    raise last_error


async def resolve_track(query: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract, query)
