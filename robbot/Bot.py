import os

import discord
from discord.ext import tasks

from robbot import logger
from robbot.db.database import PonyDB
from robbot.services.reddit import search_manga
from robbot.t import MangaChapter
from robbot.utils import format_response

db = PonyDB()


class Bot(discord.Bot):

    async def on_ready(self):
        logger.info('Logged on as', self.user)
        # await update_last_chapter()
        # self.notify_new_releases.start()

    async def close(self):
        """Logs out of Discord"""
        self.notify_new_releases.cancel()
        await super().close()
        logger.info("Closed")

    @tasks.loop(seconds=5 * 60)
    async def notify_new_releases(self):
        logger.debug("Searching for releases...")

        for channel_id in db.channel.all():
            channel = self.get_channel(int(channel_id))
            if not channel:
                logger.warning(f"channel {int(channel_id)} not found")
                continue
            releases = []
            for manga in db.manga.many(channel_id=channel_id):
                chapter = await get_new_chapter_info(manga.title)
                if chapter:
                    releases.append(format_response(chapter))
                    db.manga.update(manga.title, chapter.number)
            for release in releases:
                await channel.send(release)

        logger.info("Finished searching for releases")


async def get_new_chapter_info(title: str) -> MangaChapter | None:
    try:
        manga = db.manga.unique(title=title)
        result = await search_manga(title)
    except Exception as e:
        logger.error(f"Error while searching for {title}: {e}")
        logger.debug(f"Did not found: {title}")
        return None

    if not result:
        logger.debug(f"Did not found: {title}")
        return None

    if result.number <= manga.last_chapter:
        logger.debug(f"No new chapters for: {title} (last chapter: {manga.last_chapter})")
        return None

    if not result.link:
        logger.debug("Found new chapter but no link were provided")
        return MangaChapter(title=title, number=result.number, link=None)

    logger.debug(f"Found new chapter for: {title} (last chapter: {manga.last_chapter})")
    return MangaChapter(title=title, number=result.number, link=result.link)


async def update_last_chapter():
    for manga in db.manga.all():
        if manga.last_chapter == -1:
            result: MangaChapter = await search_manga(manga.title)
            if result:
                db.manga.update(manga.title, result.number)
    logger.info("Finished updating last chapters")


def get_bot() -> Bot:
    bot = Bot()
    guilds_ids = []

    if t := os.getenv("TESTING_GUILD_ID"):
        guilds_ids.append(t)

    @bot.slash_command(description="Get Ponged", guild_ids=guilds_ids)
    async def ping(ctx):
        await ctx.respond(f"pong {ctx.author.mention}")

    @bot.slash_command(description="Find the latest chapter for a given manga", guild_ids=guilds_ids)
    async def search(ctx, title: discord.Option(str)):
        if m := await search_manga(title):
            return await ctx.respond(f"Found {m.title} {m.number} {m.link}")
        else:
            return await ctx.respond(f"Did not found the manga {ctx.author.mention}")

    @bot.slash_command(
        description="Display the list of mangas registered on this channel",
        guild_ids=guilds_ids
    )
    async def queue(ctx):
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

    return bot
