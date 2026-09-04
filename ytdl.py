import asyncio
import os
import shutil
import yt_dlp

SECRET_COOKIES_PATH = "/etc/secrets/cookies.txt"
WRITABLE_COOKIES_PATH = "/tmp/cookies.txt"

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,

    # Search YouTube when user gives song name
    "default_search": "ytsearch1",

    # Don't spam yt-dlp output into Render logs
    "quiet": True,
    "no_warnings": False,

    # Network settings
    "nocheckcertificate": True,

    # Don't force android/web/tv.
    # Let current yt-dlp choose its supported clients.
}

# Use Render Secret File if it exists
if os.path.isfile(SECRET_COOKIES_PATH):
    try:
        shutil.copyfile(
            SECRET_COOKIES_PATH,
            WRITABLE_COOKIES_PATH
        )

        YDL_OPTS["cookiefile"] = WRITABLE_COOKIES_PATH

        print("INFO: YouTube cookies loaded.")

    except Exception as e:
        print(f"WARNING: Could not copy cookies: {e}")
else:
    print("INFO: No YouTube cookies file found.")


def _extract(query: str) -> dict:
    query = query.strip()

    if not query:
        raise ValueError("Empty search query")

    # If user gives a YouTube URL, use it directly.
    # Otherwise search YouTube.
    if query.startswith(("http://", "https://")):
        target = query
    else:
        target = f"ytsearch1:{query}"

    opts = dict(YDL_OPTS)

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(
            target,
            download=False
        )

        if not info:
            raise RuntimeError("yt-dlp returned no information")

        # ytsearch returns entries
        if "entries" in info:
            entries = info.get("entries") or []

            if not entries:
                raise RuntimeError("No results found")

            info = entries[0]

        if not info.get("url"):
            raise RuntimeError("No playable audio URL found")

        return {
            "title": info.get("title") or "Unknown",
            "url": info.get("url"),
            "webpage_url": info.get("webpage_url"),
            "duration": info.get("duration") or 0,
            "thumbnail": info.get("thumbnail"),
        }


async def resolve_track(query: str) -> dict:
    return await asyncio.to_thread(
        _extract,
        query
    )
