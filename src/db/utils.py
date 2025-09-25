import aiosqlite


async def init_db(path="data/links.db"):
    """Create database file and schema if not exists."""
    async with aiosqlite.connect(path) as db:
        await db.execute(
            """
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            message_id TEXT,
            author TEXT
        )
        """
        )
        await db.commit()
