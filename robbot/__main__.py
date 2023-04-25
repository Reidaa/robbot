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


class Main:
    def __init__(self):
        dotenv_check()
        self.bot = Bot()
        self.discord_bot_token = os.getenv("DISCORD_TOKEN")

    async def _runner(self):
        await self.bot.start(token=self.discord_bot_token, reconnect=True)

    def run(self):
        try:
            with asyncio.Runner() as runner:
                runner.run(self._runner())
        except discord.errors.LoginFailure as e:
            logger.error(e)
            return 1
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received, exiting...")
            return 0


if __name__ == "__main__":
    import sys

    sys.exit(Main().run())
