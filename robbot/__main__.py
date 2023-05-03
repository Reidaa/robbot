#! /usr/bin/env python3

"""
This module contains the main logic for the RobBot bot.
"""

import os

import robbot.log as log
from robbot.Bot import Bot
from robbot.db.database import PonyDB
from robbot.services import reddit
from robbot.utils import dotenv_check

db = PonyDB()


def update_db():
    log.info("Updating database...")
    for manga in db.manga.all():
        if manga.last_chapter == -1:
            if result := reddit.sync.search_manga(manga.title):
                log.info(f"Updating {manga.title} to chapter {result.number}")
                db.manga.update(manga.title, result.number)
            else:
                continue
        else:
            continue
    log.info("Finished updating database")


def setup():
    update_db()


class Main:
    def __init__(self):
        dotenv_check()
        self.bot = Bot()
        self.discord_bot_token = os.getenv("DISCORD_TOKEN")

        setup()

    def run(self):
        self.bot.run(self.discord_bot_token)


if __name__ == "__main__":
    import sys

    sys.exit(Main().run())
