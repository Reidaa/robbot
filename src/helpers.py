import os
import re

def is_testing():
    return True if ("test" in os.getenv("ENV")) else False


def get_chapter_number(txt: str) -> int:
    match = re.search(r'chapter\s+(\d+)', txt.lower())
    if match:
        chapter_number = match.group(1)
        return int(chapter_number)
    else:
        return -1
