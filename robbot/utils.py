import os
from pathlib import Path
from robbot.logger import debug, error
from typing import Optional


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

def user_ping(id: int) -> str:
    return f"<@{id}>"


def role_ping(id: int) -> str:
    return f"<@&{id}>"

def dotenv_check():
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / ".env"
        if not load_dotenv(dotenv_path=env_path, override=True):
            error(f"Unable to load .env file from: {env_path}")
            return 1
        else:
            debug(f"Loaded .env file from: {env_path}")
    except ImportError:
        debug("Unable to load .env file, dotenv not installed, reading from environment variables")
