import os

import discord
from discord.ext import commands

guilds_ids = []

if t := os.getenv("TESTING_GUILD_ID"):
    guilds_ids.append(t)


class BasicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(description="Get Ponged", guild_ids=guilds_ids)
    async def ping(self, ctx):
        return await ctx.respond(f"Hello, {ctx.author.mention}")


def setup(bot):
    bot.add_cog(BasicCog(bot))
