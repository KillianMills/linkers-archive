# websocket_link_collector.py
import asyncio
import websockets
import re
import aiosqlite

URL_RE = re.compile(r"(?xi)\b(?:https?://|www\.)[^\s<>()\[\]{}\'\"]+")


async def handler(uri="wss://example/chat"):
    async with aiosqlite.connect("links.db") as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, url TEXT NOT NULL UNIQUE, first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP, source TEXT)"""
        )
        await db.commit()
    async with websockets.connect(uri) as ws:
        async for message in ws:
            # assume message is JSON with text
            import json

            data = json.loads(message)
            text = data.get("text") or data.get("message") or ""
            for u in set(URL_RE.findall(text)):
                from urllib.parse import urlparse, urlunparse

                def normalise_url(url):
                    url = url.rstrip(".,;:!)\"']")
                    if url.startswith("www."):
                        url = "http://" + url
                    p = urlparse(url)
                    netloc = p.netloc.lower().replace(":80", "").replace(":443", "")
                    path = p.path or "/"
                    return urlunparse((p.scheme, netloc, path, p.params, p.query, ""))

                n = normalise_url(u)
                async with aiosqlite.connect("links.db") as db:
                    await db.execute(
                        "INSERT OR IGNORE INTO links (url, source) VALUES (?,?)",
                        (n, "websocket"),
                    )
                    await db.commit()


if __name__ == "__main__":
    asyncio.run(handler("wss://your-chat.example/ws"))
