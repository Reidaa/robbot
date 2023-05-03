import discord
from discord.ext import tasks

from robbot import logger
from robbot.db.database import PonyDB
from robbot.services.reddit import search_manga
from robbot.t import MangaChapter
from robbot.utils import format_response

db = PonyDB()


class Bot(discord.Bot):
    def __init__(self):
        super().__init__()
        self.load_extension("robbot.cogs.Basic")
        self.load_extension("robbot.cogs.Manga")

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
