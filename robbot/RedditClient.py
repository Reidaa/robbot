import asyncio
import os
from typing import List

import asyncpraw
from asyncpraw.models import Submission

from robbot.utils import get_chapter_number


class RedditClient:
    def __init__(self):
        self.reddit: asyncpraw.Reddit = asyncpraw.Reddit(
            client_id=os.getenv("REDDIT_ID"),
            client_secret=os.getenv("REDDIT_SECRET"),
            user_agent=os.getenv("REDDIT_AGENT")
        )

    async def search_subreddit(self, subreddit: str, query: str, sort: str = "relevance", limit: int = 100) -> List[
        Submission]:
        submissions = []
        subreddit = await self.reddit.subreddit(subreddit)
        search_result = subreddit.search(query, sort=sort, limit=limit)
        async for post in search_result:
            submissions.append(post)
        return submissions

    def __del__(self):
        async def task():
            await self.reddit.close()

        loop = asyncio.get_event_loop()
        loop.create_task(task())


async def search_manga(title: str) -> dict | None:
    def filter_fun(x: Submission):
        title = x.title.lower()
        if "[disc]" in title and "chapter" in title:
            return x

    unfiltered = await RedditClient().search_subreddit(subreddit="manga", query=f"[disc] {title}")
    results = list(filter(filter_fun, unfiltered))
    chapter_list = [get_chapter_number(submission.title) for submission in results]
    last_chapter = max(chapter_list)
    idx = chapter_list.index(last_chapter)
    return {
        "title": results[idx].title[7:],
        "chapter": last_chapter,
        "link": results[idx].url
    }
