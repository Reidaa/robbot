from pathlib import Path
from typing import Optional

from robbot import logger
from robbot.db.ponydb import DB
from robbot.services.reddit import search_manga
from robbot.t import SearchMangaResult, MangaChapter


def get_chapter_number(chapter_title) -> Optional[int]:
    digits = ""
    for c in reversed(chapter_title.rstrip()):
        if c.isdigit():
            digits = c + digits
        elif digits:
            break
    if digits:
        return int(digits)
    else:
        return None


def format_user_ping(id: int) -> str:
    return f"<@{id}>"


def format_role_ping(id: int) -> str:
    return f"<@&{id}>"


def dotenv_check():
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / ".env"
        if not load_dotenv(dotenv_path=env_path, override=True):
            logger.error(f"Unable to load .env file from: {env_path}")
            return 1
        else:
            logger.debug(f"Loaded .env file from: {env_path}")
    except ImportError:
        logger.debug("Unable to load .env file, dotenv not installed, reading from environment variables")


async def update_last_chapter():
    for manga in DB.get_mangas():
        if manga.last_chapter == -1:
            result: SearchMangaResult = await search_manga(manga.title)
            if result:
                DB.update_manga_chapter(manga.title, result.chapter)
    logger.info("Finished updating last chapters")


def format_response(chapter: MangaChapter) -> str:
    if chapter.link:
        return f"{chapter.title} {chapter.number}: {chapter.link}"
    else:
        return f"A new chapter for {chapter.title} was found but no link were provided"


async def get_new_chapter_info(title: str) -> MangaChapter | None:
    try:
        manga = DB.get_manga_from_title(title)
        result = await search_manga(title)
    except Exception as e:
        logger.error(f"Error while searching for {title}: {e}")
        logger.debug(f"Did not found: {title}")
        return None

    if not result:
        logger.debug(f"Did not found: {title}")
        return None

    if result.chapter <= manga.last_chapter:
        logger.debug(f"No new chapters for: {title} (last chapter: {manga.last_chapter})")
        return None

    if not result.link:
        logger.debug("Found new chapter but no link were provided")
        return MangaChapter(title=title, number=result.chapter, link=None)

    logger.debug(f"Found new chapter for: {title} (last chapter: {manga.last_chapter})")
    return MangaChapter(title=title, number=result.chapter, link=result.link)
