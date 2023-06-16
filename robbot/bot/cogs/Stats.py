import os

from discord.ext import commands, tasks

from robbot import log

guilds_ids: list | None = []

if t := os.getenv("TESTING_GUILD_ID"):
    guilds_ids.append(t)
else:
    guilds_ids = None


class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.server_count = 0
        self.user_count = 0

        self.update_stats.start()

    @tasks.loop(hours=12)
    async def update_stats(self):
        log.debug("Updating stats...")
        self.server_count = len(self.bot.guilds)
        self.user_count = len(self.bot.users)
