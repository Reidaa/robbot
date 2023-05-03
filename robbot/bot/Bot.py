import logging

import discord
from discord.ext import tasks

from robbot import log
from robbot.db.database import PonyDB
from robbot.services import reddit
from robbot.t import MangaChapter
from robbot.utils import format_response

db = PonyDB()


class Bot(discord.Bot):
    def __init__(self):
        super().__init__()
        log.get_logger("discord", stderr=True).setLevel(logging.DEBUG)
        # self.load_extension("robbot.bot.cogs.Basic")
        self.load_extension("robbot.bot.cogs.Manga")

    async def on_ready(self):
        log.info('Logged on as', self.user)
        self.notify_new_releases.start()

    async def close(self):
        """Logs out of Discord"""
        self.notify_new_releases.cancel()
        await super().close()
        log.info("Closed")

    @tasks.loop(seconds=5 * 60)
    async def notify_new_releases(self):
        log.debug("Searching for releases...")

        for channel_id in db.channel.all():
            channel = self.get_channel(int(channel_id))
            if not channel:
                log.warning(f"channel {int(channel_id)} not found")
                continue
            releases = []
            for manga in db.manga.many(channel_id=channel_id):
                chapter = await get_new_chapter_info(manga.title)
                if chapter:
                    releases.append(format_response(chapter))
                    db.manga.update(manga.title, chapter.number)
            for release in releases:
                await channel.send(release)

        log.info("Finished searching for releases")


async def get_new_chapter_info(title: str) -> MangaChapter | None:
    if not (manga := db.manga.unique(title=title)):
        log.error(f"Error while searching for {title}: Manga not registered")
        log.debug(f"Did not found: {title}")
        return None

    try:
        result = await reddit.notsync.search_manga(title)
    except Exception as e:
        log.error(f"Error while searching for {title}: {e}")
        log.debug(f"Did not found: {title}")
        return None

    if not result:
        log.debug(f"Did not found: {title}")
        return None

    if result.number <= manga.last_chapter:
        log.debug(f"No new chapters for: {title} (last chapter: {manga.last_chapter})")
        return None

    if not result.link:
        log.debug("Found new chapter but no link were provided")
        return MangaChapter(title=title, number=result.number, link=None)

    log.debug(f"Found new chapter for: {title} (last chapter: {manga.last_chapter})")
    return MangaChapter(title=title, number=result.number, link=result.link)
