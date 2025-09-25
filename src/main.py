import os
import asyncio
from dotenv import load_dotenv

# import collectors
# import collectors
from src.collectors import discord_collector

# later you can also import twitch_collector, websocket_collector, etc.


async def main():
    print("Starting link collectors...")
    load_dotenv()  # load .env file if present
    mode = os.getenv("COLLECTOR_MODE", "discord")

    if mode == "discord":
        try:
            await discord_collector.run()
        except RuntimeError as e:
            # Print a friendly message and exit with non-zero status
            print(f"Collector failed: {e}")
            return
    else:
        print(f"Unknown COLLECTOR_MODE: {mode}")


if __name__ == "__main__":
    print("running main")
    asyncio.run(main())
