import os
from typing import Optional

from asyncpraw import Reddit
from asyncpraw.models import Submission

from robbot.utils import get_chapter_number
from robbot.t import SearchMangaResult
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
    

async def search_manga(query: str) -> Optional[SearchMangaResult]:
    logger.debug(f"searching |{query}| on r/manga")
    ret: Optional[SearchMangaResult] = None
    chapters: list[int] = []

    def filter_fun(x: Submission):
        title = x.title.lower()
        if any(substring in title for substring in ["chapter", "ch"]):
            substrings = query.lower().split() + ["[disc]"]
            if all(substring in title for substring in substrings):
                return x

    unfiltered = await search_subreddit(subreddit="manga", query=f"[disc] {query}")
    filtered = list(filter(filter_fun, unfiltered))
    if len(filtered) != 0:
        for submission in filtered:
            if t := get_chapter_number(submission.title):
                chapters.append(t)
        last_chapter = max(chapters)
        idx: int = chapters.index(last_chapter)

        if filtered[idx].title.startswith("[DISC]"):
            logger.debug("found something")
            ret = SearchMangaResult(
                title=filtered[idx].title[7:],
                chapter=last_chapter,
                link=filtered[idx].url
            )
        else:
            logger.debug("found nothing")
    else:
        pass
        
    return ret