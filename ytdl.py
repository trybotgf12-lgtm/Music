import asyncio
import json
import logging
import re
import time
import urllib.request
import yt_dlp

log = logging.getLogger("ytdl")

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "scsearch",
    "geo_bypass": True,
    "nocheckcertificate": True,
}

SPOTIFY_URL_RE = re.compile(r"open\.spotify\.com/track/([A-Za-z0-9]+)")


def _spotify_track_name(url: str) -> str:
    oembed_url = f"https://open.spotify.com/oembed?url={url}"
    with urllib.request.urlopen(oembed_url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    title = data.get("title", "")
    artist = data.get("author_name", "")
    return f"{title} {artist}".strip()


def _resolve_query(query: str) -> str:
    match = SPOTIFY_URL_RE.search(query)
    if match:
        try:
            name = _spotify_track_name(query)
            log.info(f"Spotify link resolved to search: {name}")
            return name
        except Exception as e:
            log.warning(f"Could not resolve Spotify link, using raw query: {e}")
    return query


def _extract(query: str) -> dict:
    query = _resolve_query(query)
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
            log.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1.5)
    raise last_error


async def resolve_track(query: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract, query)
