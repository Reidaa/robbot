#! /usr/bin/env python3

"""
This module contains the main logic for the RobBot bot.
"""

import asyncio
import os

import discord

from robbot import logger
from robbot.Bot import Bot
from robbot.utils import dotenv_check


def main():
    dotenv_check()
    discord_bot_token = os.getenv("DISCORD_TOKEN")
    bot = Bot()

    async def runner():
        async with bot:
            await bot.start(token=discord_bot_token, reconnect=True)

    try:
        asyncio.run(runner())
    except discord.errors.LoginFailure as e:
        logger.error(e)
        return 1
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, exiting...")
        return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())