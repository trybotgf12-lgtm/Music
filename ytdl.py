import asyncio
import os
import shutil
import time
import yt_dlp

SECRET_COOKIES_PATH = "/etc/secrets/cookies.txt"
WRITABLE_COOKIES_PATH = "/tmp/cookies.txt"

BASE_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
}

if os.path.exists(SECRET_COOKIES_PATH):
    shutil.copyfile(SECRET_COOKIES_PATH, WRITABLE_COOKIES_PATH)
    BASE_OPTS["cookiefile"] = WRITABLE_COOKIES_PATH


def _try_source(query: str, search_prefix: str) -> dict:
    opts = dict(BASE_OPTS)
    opts["default_search"] = search_prefix
    with yt_dlp.YoutubeDL(opts) as ydl:
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


def _extract(query: str) -> dict:
    is_url = query.startswith("http://") or query.startswith("https://")

    # 1) Try YouTube first (with retries, since it's intermittently broken)
    last_error = None
    for attempt in range(3):
        try:
            return _try_source(query, "ytsearch")
        except Exception as e:
            last_error = e
            time.sleep(1.5)

    # 2) If it was a plain search (not a direct URL), fall back to SoundCloud
    if not is_url:
        try:
            return _try_source(query, "scsearch")
        except Exception:
            pass

    raise last_error


async def resolve_track(query: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract, query)
