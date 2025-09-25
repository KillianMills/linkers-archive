import os
import re
import logging
import discord
import aiosqlite
from urllib.parse import urlparse, urlunparse
from ..db.utils import init_db

URL_RE = re.compile(r"(?xi)\b(?:https?://|www\.)[^\s<>()\[\]{}\'\"]+")


def normalise_url(url: str) -> str:
    """Clean and normalise URLs before storing in DB."""
    url = url.rstrip(".,;:!?)\"']")
    if url.startswith("www."):
        url = "http://" + url
    p = urlparse(url)
    netloc = p.netloc.lower().replace(":80", "").replace(":443", "")
    path = p.path or "/"
    return urlunparse((p.scheme, netloc, path, p.params, p.query, ""))


async def run():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Missing DISCORD_TOKEN in .env file")

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logging.info(f"Logged in as {client.user}")
        await init_db("data/links.db")

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        found = URL_RE.findall(message.content or "")
        if not found:
            return

        normalized = {normalise_url(u) for u in found}

        async with aiosqlite.connect("data/links.db") as db:
            for u in normalized:
                try:
                    # Check whether this URL already exists so we can log only when
                    # a new row is actually inserted (gives immediate console feedback).
                    cur = await db.execute("SELECT 1 FROM links WHERE url = ? LIMIT 1", (u,))
                    exists = await cur.fetchone()
                    if exists:
                        logging.debug(f"URL already exists, skipping: {u}")
                        continue

                    await db.execute(
                        """
                        INSERT INTO links
                        (url, source, message_id, author)
                        VALUES (?, ?, ?, ?)
                        """,
                        (u, "discord", str(message.id), str(message.author)),
                    )
                    # Log successful insert so the console shows captured URLs live.
                    logging.info(
                        "Saved URL: %s (source=%s author=%s message_id=%s)",
                        u,
                        "discord",
                        str(message.author),
                        str(message.id),
                    )
                except Exception:
                    logging.exception(f"DB insert failed for {u}")
            await db.commit()

    logging.basicConfig(level=logging.INFO)
    # Use start() which is an awaitable coroutine instead of client.run(),
    # so we don't call asyncio.run() from inside an existing event loop.
    try:
        await client.start(token)
    except discord.errors.PrivilegedIntentsRequired as exc:
        # Provide a clear, actionable error message when privileged intents
        # (for example message content) are not enabled in the developer portal.
        logging.error(
            "Discord privileged intents required: %s.\n"
            "Please enable the required privileged intents (Message Content / Presence) "
            "for your application at https://discord.com/developers/applications/",
            exc,
        )
        # Try to close the client to avoid leaking the aiohttp connector/session.
        try:
            await client.close()
        except Exception:
            pass

        # As a fallback, try to start the bot with message_content disabled so
        # the bot can at least come online in a degraded mode (it won't receive
        # raw message content, so the URL collection will not run).
        logging.info(
            "Retrying without message_content intent (degraded mode). "
            "URLs will not be collected until Message Content intent is enabled."
        )
        try:
            reduced_intents = discord.Intents.default()
            reduced_intents.message_content = False
            client = discord.Client(intents=reduced_intents)

            @client.event
            async def on_ready():
                logging.info(f"Logged in (degraded mode) as {client.user}")

            # Keep the on_message handler in place, but it will not receive
            # message content when message_content is False.
            @client.event
            async def on_message(message):
                # If message content isn't available, message.content will be ''
                # or an empty value; we still guard for bots.
                if message.author.bot:
                    return

            await client.start(token)
        except Exception as e:
            logging.exception("Failed to start Discord client even in degraded mode")
            raise RuntimeError(
                "Discord client could not start. Check bot token and intents in the developer portal."
            )
