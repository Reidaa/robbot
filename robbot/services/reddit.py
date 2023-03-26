import asyncio
import os
from typing import Optional

from asyncpraw import Reddit
from asyncpraw.models import Submission

from robbot.utils import get_chapter_number
from robbot.types import SearchMangaResult
from robbot import logger


async def search_subreddit(subreddit: str, query: str, sort: str = "relevance", limit: int = 100) -> list[Submission]:
        logger.debug(f"searching {subreddit} for '{query}' with sort '{sort}'and limit '{limit}'")
        submissions = []
        async with Reddit(
                client_id=os.getenv("REDDIT_ID"), 
                client_secret=os.getenv("REDDIT_SECRET"), 
                user_agent=os.getenv("REDDIT_AGENT")
            ) as reddit:
            subreddit = await reddit.subreddit(subreddit)
            search_result = subreddit.search(query, sort=sort, limit=limit)
            async for post in search_result:
                submissions.append(post)
        return submissions
    

async def search_manga(title: str) -> Optional[SearchMangaResult]:
    logger.debug(f"searching |{title}| on r/manga")
    ret: Optional[SearchMangaResult] = None
    chapters: list[int] = []

    def filter_fun(x: Submission):
        title = x.title.lower()
        if "[disc]" in title and ("chapter" in title or "ch" in title):
            return x

    unfiltered = await search_subreddit(subreddit="manga", query=f"[disc] {title}")
    results = list(filter(filter_fun, unfiltered))
    # chapter_list = [get_chapter_number(submission.title) for submission in results]
    for submission in results:
        if t := get_chapter_number(submission.title):
            chapters.append(t)
    last_chapter = max(chapters)
    idx: int = chapters.index(last_chapter)

    if results[idx].title.startswith("[DISC]"):
        logger.debug("found something")
        ret = SearchMangaResult(
            title=results[idx].title[7:],
            chapter=last_chapter,
            link=results[idx].url
        )
    else:
        logger.debug("found nothing")
        
        
    return ret