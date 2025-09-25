import os
import asyncio
from dotenv import load_dotenv

# import collectors
# import collectors
from linkers_archive.collectors import discord_collector
# later you can also import twitch_collector, websocket_collector, etc.

async def main():
    print("Starting link collectors...")
    load_dotenv()  # load .env file if present
    mode = os.getenv("COLLECTOR_MODE", "discord")

    if mode == "discord":
        await discord_collector.run()
    else:
        print(f"Unknown COLLECTOR_MODE: {mode}")

if __name__ == "__main__":
    print('running main')
    asyncio.run(main())
