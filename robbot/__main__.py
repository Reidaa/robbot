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

    # log_handler: Optional[logging.Handler] = MISSING
    # log_formatter: Optional[logging.Formatter] = MISSING
    # log_level: int = MISSING
    # root_logger: bool = False
    # if log_handler is not None:
    #     utils.setup_logging(
    #         handler=log_handler,
    #         formatter=log_formatter,
    #         level=log_level,
    #         root=root_logger,
    #     )

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