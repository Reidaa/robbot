import os

import discord
from discord.ext import commands

from robbot.db.database import PonyDB
from robbot.services import reddit

db = PonyDB()

guilds_ids = []

if t := os.getenv("TESTING_GUILD_ID"):
    guilds_ids.append(t)


class Manga(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(description="Find the latest chapter for a given manga", guild_ids=guilds_ids)
    @discord.option("title", type=str, description="The title of the manga to search for", required=True)
    async def search(self, ctx, title: str):
        if m := await reddit.notsync.search_manga(title):
            return await ctx.respond(f"Found {m.title} {m.number} {m.link}")
        else:
            return await ctx.respond(f"Did not found the manga {ctx.author.mention}")

    @discord.slash_command(
        description="Display the list of mangas registered on this channel",
        guild_ids=guilds_ids
    )
    async def queue(self, ctx: discord.ApplicationContext):
        channel_id = ctx.channel_id
        response = []

        if mangas := db.manga.many(channel_id=channel_id):
            for manga in mangas:
                response.append(f"{manga.title}")
            return await ctx.respond("\n".join(response))
        else:
            return await ctx.respond("Nothing registered")

    # @bot.slash_command(
    #     description="Register a manga to receive notifications when a new chapter is released",
    #     guild_ids=guilds_ids
    # )
    # async def register(ctx, title: discord.Option(str)):
    #     def check(reaction: discord.Reaction, user):
    #         if user != ctx.user:
    #             return False
    #         if str(reaction.emoji) not in ["✅", "❌"]:
    #             return False
    #         return True
    #
    #     await ctx.respond("Searching...")
    #
    #     if r := DB.get_mangas(channel_id=ctx.channel_id):
    #         for manga in r:
    #             if manga.title.lower() == title.lower():
    #                 return await ctx.respond(f"{title} is already registered")
    #
    #     if r := DB.get_manga(title=title):
    #         pass
    #         return await ctx.respond(f"Registered {title}")
    #
    #     if searched := await search_manga(title):
    #         message = await ctx.respond(
    #             f"Found:\n{searched.title} {searched.chapter}\n{searched.link}, is this correct ?")
    #         await message.add_reaction("✅")
    #         await message.add_reaction("❌")
    #
    #         try:
    #             reaction, user = await bot.wait_for("reaction_add", check=check, timeout=30)
    #         except TimeoutError:
    #             return await ctx.respond("Timeout-ed")
    #         else:
    #             if str(reaction.emoji) == "❌":
    #                 return await ctx.respond("Canceling registration")
    #             else:
    #                 return await ctx.respond(f"Registered {title}")
    #     else:
    #         return await ctx.respond(f"Did not found {title}")

    # manga = DB.get_manga_from_title(title)
    #
    # if manga:
    #     DB.update_manga_channel(title, channel_id)
    # else:
    #     DB.add_manga(title, channel_id)


def setup(bot):
    bot.add_cog(Manga(bot))
