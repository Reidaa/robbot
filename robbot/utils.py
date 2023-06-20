from pathlib import Path
from typing import Optional

from robbot import log
from robbot.t import S_MangaChapter


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


def format_user_ping(user_id: int) -> str:
    return f"<@{user_id}>"


def format_role_ping(role_id: int) -> str:
    return f"<@&{role_id}>"


def dotenv_check():
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / ".env"
        if not load_dotenv(dotenv_path=env_path, override=True):
            log.error(f"Unable to load .env file from: {env_path}")
        else:
            log.debug(f"Loaded .env file from: {env_path}")
    except ImportError:
        log.debug("Unable to load .env file, dotenv not installed, reading from environment variables")


def format_response(chapter: S_MangaChapter) -> str:
    if chapter.link:
        return f"{chapter.title} {chapter.number}: {chapter.link}"
    else:
        return f"A new chapter for {chapter.title} was found but no link were provided"
