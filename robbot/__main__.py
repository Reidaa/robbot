#! /usr/bin/env python3

"""
This module contains the main logic for the RobBot bot.
"""

import os

from robbot.Bot import get_bot
from robbot.utils import dotenv_check


class Main:
    def __init__(self):
        dotenv_check()
        self.bot = get_bot()
        self.discord_bot_token = os.getenv("DISCORD_TOKEN")

    def run(self):
        self.bot.run(self.discord_bot_token)


if __name__ == "__main__":
    import sys

    sys.exit(Main().run())
