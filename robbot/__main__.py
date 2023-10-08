#! /usr/bin/env python3

"""
This module contains the main logic for the RobBot bot.
"""

import os

from robbot.utils import dotenv_check

dotenv_check()

import robbot.log as log
from robbot.bot.Bot import Bot
from robbot.services import reddit



# def update_db():
#     log.info("Updating database...")
#     for manga in db.manga.all():
#         if manga.last_chapter == -1:
#             if r := reddit.sync.search_manga(manga.title):
#                 log.info(f"Updating {manga.title} to chapter {r.number}")
#                 db.manga.update(manga.title, r.number)
#             else:
#                 continue
#         else:
#             continue
#     log.info("Finished updating database")


def setup():
    # update_db()
    pass

class Main:
    def __init__(self):
        self.bot = Bot()
        self.discord_bot_token = os.getenv("DISCORD_TOKEN")

        setup()

    def run(self):
        self.bot.run(self.discord_bot_token)


if __name__ == "__main__":
    import sys

    sys.exit(Main().run())
