import asyncio
import os
from typing import Optional

# from asyncpraw import Reddit
# from asyncpraw.models import Submission
from praw import Reddit
from praw.models import Submission

from robbot.utils import get_chapter_number
from robbot.types import SearchMangaResult


async def search_subreddit(subreddit: str, query: str, sort: str = "relevance", limit: int = 100) -> list[Submission]:
        logger.debug(f"searching {subreddit} for {query} with sort {sort} and limit {limit}")
        submissions = []
        async with Reddit(
            client_id=os.getenv("REDDIT_ID"),
            client_secret=os.getenv("REDDIT_SECRET"),
            user_agent=os.getenv("REDDIT_AGENT")
            ) as reddit:
            subreddit = reddit.subreddit(subreddit)
            search_result = subreddit.search(query, sort=sort, limit=limit)
            async for post in search_result:
                submissions.append(post)
        return submissions
    

async def search_manga(title: str) -> Optional[SearchMangaResult]:
    def filter_fun(x: Submission):
        title = x.title.lower()
        if "[disc]" in title and "chapter" in title:
            return x

    logger.debug(f"searching for {title} on reddit")
    unfiltered = await search_subreddit(subreddit="manga", query=f"[disc] {title}")
    results = list(filter(filter_fun, unfiltered))
    chapter_list = [get_chapter_number(submission.title) for submission in results]
    last_chapter = max(chapter_list)
    idx = chapter_list.index(last_chapter)
    ret: Optional[SearchMangaResult] = None

    if results[idx].title.startswith("[DISC]"):
        logger.debug("found something")
        ret = SearchMangaResult(
            title=results[idx].title[7:],
            chapter=last_chapter,
            link=result[idx].url if result[idx].url else None
        )
    else:
        logger.debug("found nothing")
        
        
    return ret