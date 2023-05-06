import logging

import discord

from robbot import log


class Bot(discord.Bot):
    def __init__(self):
        super().__init__()
        log.get_logger("discord", stderr=True).setLevel(logging.DEBUG)
        # self.load_extension("robbot.bot.cogs.Basic")
        self.load_extension("robbot.bot.cogs.Manga")

    async def on_ready(self):
        log.info('Logged on as', self.user)
