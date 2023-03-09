import os
import random
import re
from datetime import datetime, timedelta
from typing import Dict, Callable


def cooldown(duration: float):
    last_called: Dict[Callable, datetime] = {}

    def decorator(wrapped: Callable):
        async def wrapper(*args, **kwargs):
            # Check when the function was last called
            now = datetime.now()
            if (wrapped in last_called) and (now - last_called[wrapped] < timedelta(seconds=duration)):
                return  # Do nothing

            # Call the wrapped function and update the last called time
            result = await wrapped(*args, **kwargs)
            last_called[wrapped] = now
            return result

        return wrapper

    return decorator


def random_number() -> int:
    return random.randint(0, 100)


def is_testing():
    return True if ("test" in os.getenv("ENV")) else False


def get_chapter_number(txt: str) -> int:
    match = re.search(r'chapter\s+(\d+)', txt.lower())
    if match:
        chapter_number = match.group(1)
        return int(chapter_number)
    else:
        return -1


def is_citation(txt: str) -> bool:
    match = re.match(r"^([A-Za-z]+):\s*", txt)
    if match:
        return True
    else:
        return False
