import os
import asyncio
from dotenv import load_dotenv
import sys
import logging

# import collectors
# import collectors
from src.collectors import discord_collector

# later you can also import twitch_collector, websocket_collector, etc.


async def main():
    print("Starting link collectors...")
    load_dotenv()  # load .env file if present

    # Respect LOG_LEVEL if provided (but don't log secrets)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

    # Minimal pre-flight checks: ensure required env vars are present
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print(
            "ERROR: DISCORD_TOKEN is not set.\n"
            "Create a local `.env` from `.env.example` and add your bot token, or set the DISCORD_TOKEN environment variable.\n"
            "See .env.example for required variables."
        )
        # Exit with non-zero status so CI / supervisors know startup failed
        sys.exit(1)

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
