import os

from asyncpraw import Reddit
from asyncpraw.models import Submission
from praw import Reddit as SyncReddit
from praw.models import Submission as SyncSubmission

from robbot import log
from robbot.t import MangaChapter
from robbot.utils import get_chapter_number


def filter_post(query: str, posts: list[Submission | SyncSubmission]):
    def filter_fun(x: Submission | SyncSubmission):
        title = x.title.lower()
        if any(substring in title for substring in ["chapter", "ch"]):
            substrings = query.lower().split() + ["[disc]"]
            if all(substring in title for substring in substrings):
                return x

    chapters: list[int] = []
    chapter: MangaChapter | None = None

    filtered = list(filter(filter_fun, posts))
    if len(filtered) != 0:
        for submission in filtered:
            if t := get_chapter_number(submission.title):
                chapters.append(t)
            else:
                continue
        last_chapter = max(chapters)
        idx: int = chapters.index(last_chapter)

        if filtered[idx].title.lower().startswith("[disc]"):
            chapter = MangaChapter(
                title=filtered[idx].title[7:],
                number=last_chapter,
                link=filtered[idx].url
            )
        else:
            pass
    else:
        pass

    return chapter


class notsync:
    @staticmethod
    async def search_subreddit(subreddit: str, query: str, sort: str = "relevance", limit: int = 100) -> list[
        Submission]:
        log.debug(f"searching {subreddit} for '{query}' with sort '{sort}'and limit '{limit}'")
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

    @staticmethod
    async def search_manga(query: str) -> MangaChapter | None:
        log.debug(f"searching |{query}| on r/manga")
        unfiltered = await notsync.search_subreddit(subreddit="manga", query=f"[disc] {query}")
        return filter_post(query, unfiltered)


class sync:

    @staticmethod
    def search_subreddit(subreddit: str, query: str, sort: str = "relevance", limit: int = 100) -> list[
        SyncSubmission]:
        log.debug(f"searching {subreddit} for '{query}' with sort '{sort}'and limit '{limit}'")
        submissions = []
        with SyncReddit(
                client_id=os.getenv("REDDIT_ID"),
                client_secret=os.getenv("REDDIT_SECRET"),
                user_agent=os.getenv("REDDIT_AGENT")
        ) as reddit:
            subreddit = reddit.subreddit(subreddit)
            search_result = subreddit.search(query, sort=sort, limit=limit)
            for post in search_result:
                submissions.append(post)
        return submissions

    @staticmethod
    def search_manga(query: str) -> MangaChapter | None:
        log.debug(f"searching |{query}| on r/manga")

        unfiltered = sync.search_subreddit(subreddit="manga", query=f"[disc] {query}")
        return filter_post(query, unfiltered)
