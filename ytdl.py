import asyncio
import os
import shutil
import time
import yt_dlp

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
    "extractor_args": {"youtube": {"player_client": ["default", "web_embedded"]}},
}

print(f"DEBUG: checking cookies at {SECRET_COOKIES_PATH}", flush=True)
if os.path.exists(SECRET_COOKIES_PATH):
    size = os.path.getsize(SECRET_COOKIES_PATH)
    print(f"DEBUG: cookies file FOUND, size={size} bytes", flush=True)
    shutil.copyfile(SECRET_COOKIES_PATH, WRITABLE_COOKIES_PATH)
    YDL_OPTS["cookiefile"] = WRITABLE_COOKIES_PATH
else:
    print("DEBUG: cookies file NOT FOUND at that path!", flush=True)


def _extract(query: str) -> dict:
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
            time.sleep(1.5)
    raise last_error


async def resolve_track(query: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract, query)
