import asyncio
import os
import shutil
import yt_dlp

SECRET_COOKIES_PATH = "/etc/secrets/cookies.txt"
WRITABLE_COOKIES_PATH = "/tmp/cookies.txt"

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "default_search": "ytsearch1",

    "quiet": True,
    "no_warnings": False,

    "nocheckcertificate": True,

    "extractor_args": {
        "youtube": {
            "player_client": ["default", "web_embedded"]
        }
    },
}

# Load Render Secret File if available
if os.path.isfile(SECRET_COOKIES_PATH):
    try:
        shutil.copyfile(
            SECRET_COOKIES_PATH,
            WRITABLE_COOKIES_PATH
        )

        YDL_OPTS["cookiefile"] = WRITABLE_COOKIES_PATH

        print("INFO: YouTube cookies loaded.", flush=True)

    except Exception as e:
        print(
            f"WARNING: Could not load YouTube cookies: {e}",
            flush=True
        )
else:
    print(
        "INFO: YouTube cookies file not found.",
        flush=True
    )


def _extract(query: str) -> dict:
    query = query.strip()

    if not query:
        raise ValueError("Empty search query")

    # Direct URL or YouTube search
    if query.startswith(("http://", "https://")):
        target = query
    else:
        target = f"ytsearch1:{query}"

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:

        info = ydl.extract_info(
            target,
            download=False
        )

        if not info:
            raise RuntimeError(
                "yt-dlp returned no information"
            )

        # Search result
        if "entries" in info:
            entries = info.get("entries") or []

            if not entries:
                raise RuntimeError(
                    "No results found"
                )

            info = entries[0]

        audio_url = info.get("url")

        if not audio_url:
            raise RuntimeError(
                "No playable audio URL found"
            )

        return {
            "title": info.get(
                "title",
                "Unknown"
            ),
            "url": audio_url,
            "webpage_url": info.get(
                "webpage_url"
            ),
            "duration": info.get(
                "duration",
                0
            ),
            "thumbnail": info.get(
                "thumbnail"
            ),
        }


async def resolve_track(query: str) -> dict:
    return await asyncio.to_thread(
        _extract,
        query
    )
