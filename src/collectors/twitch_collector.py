# twitch_link_collector.py
import socket
import re
import time
import aiosqlite
import asyncio
from urllib.parse import urlparse, urlunparse

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "your_twitch_username"
TOKEN = "oauth:your_oauth_token"  # get from https://twitchapps.com/tmi/
CHANNEL = "#target_channel"

URL_RE = re.compile(r"(?xi)\b(?:https?://|www\.)[^\s<>()\[\]{}\'\"]+")


def normalise_url(url):
    url = url.rstrip(".,;:!?)\"']")
    if url.startswith("www."):
        url = "http://" + url
    p = urlparse(url)
    netloc = p.netloc.lower().replace(":80", "").replace(":443", "")
    path = p.path or "/"
    return urlunparse((p.scheme, netloc, path, p.params, p.query, ""))


async def ensure_db():
    async with aiosqlite.connect("links.db") as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS links (
			id INTEGER PRIMARY KEY, url TEXT NOT NULL UNIQUE, first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP, source TEXT)"""
        )
        await db.commit()


async def run():
    await ensure_db()
    s = socket.socket()
    s.connect((HOST, PORT))
    s.sendall(f"PASS {TOKEN}\r\n".encode())
    s.sendall(f"NICK {NICK}\r\n".encode())
    s.sendall(f"JOIN {CHANNEL}\r\n".encode())
    buf = ""
    try:
        while True:
            data = s.recv(1024).decode(errors="ignore")
            if not data:
                break
            buf += data
            while "\r\n" in buf:
                line, buf = buf.split("\r\n", 1)
                if line.startswith("PING"):
                    s.sendall("PONG :tmi.twitch.tv\r\n".encode())
                # parse message text (simple)
                parts = line.split("PRIVMSG", 1)
                if len(parts) > 1:
                    msg = parts[1].split(":", 1)[1]
                    found = URL_RE.findall(msg)
                    if found:
                        normalized = {normalise_url(u) for u in found}
                        async with aiosqlite.connect("links.db") as db:
                            for u in normalized:
                                await db.execute(
                                    "INSERT OR IGNORE INTO links (url, source) VALUES (?, ?)",
                                    (u, "twitch"),
                                )
                            await db.commit()
    finally:
        s.close()


if __name__ == "__main__":
    asyncio.run(run())
