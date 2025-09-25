import os
import re
import logging
import discord
import aiosqlite
from urllib.parse import urlparse, urlunparse
from linkers_archive.data.utils import init_db

URL_RE = re.compile(r'(?xi)\b(?:https?://|www\.)[^\s<>()\[\]{}\'\"]+')

def normalise_url(url: str) -> str:
	"""Clean and normalise URLs before storing in DB."""
	url = url.rstrip('.,;:!?)"\']')
	if url.startswith('www.'):
		url = 'http://' + url
	p = urlparse(url)
	netloc = p.netloc.lower().replace(':80', '').replace(':443', '')
	path = p.path or '/'
	return urlunparse((p.scheme, netloc, path, p.params, p.query, ''))

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
					await db.execute(
						"""
						INSERT OR IGNORE INTO links
						(url, source, message_id, author)
						VALUES (?, ?, ?, ?)
						""",
						(u, "discord", str(message.id), str(message.author)),
					)
				except Exception as e:
					logging.exception(f"DB insert failed for {u}")
			await db.commit()

	logging.basicConfig(level=logging.INFO)
	client.run(token)
