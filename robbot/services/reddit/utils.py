import os

from asyncpraw import Reddit
from asyncpraw.models import Submission

from robbot import log
from .models import MangaChapter
from robbot.utils import get_chapter_number


def _filter_post(query: str, posts: list[Submission]) -> MangaChapter | None:
    def filter_fun(x: Submission):
        title = x.title.lower()
        if any(substring in title for substring in ["chapter", "ch"]):
            substrings = query.lower().split() + ["[disc]"]
            if all(substring in title for substring in substrings):
                return x

    chapters: list[int] = []

    filtered = list(filter(filter_fun, posts))

    if len(filtered) == 0:
        return None

    for submission in filtered:
        if t := get_chapter_number(submission.title):
            chapters.append(t)
        else:
            continue
    last_chapter = max(chapters)
    idx: int = chapters.index(last_chapter)

    if not filtered[idx].title.lower().startswith("[disc]"):
        return None

    chapter = MangaChapter(
        manga_title=filtered[idx].title[7:],
        number=last_chapter,
        link=filtered[idx].url
    )

    return chapter


async def _async_search_subreddit(subreddit_name: str, query: str, sort: str = "relevance", limit: int = 100) -> \
        list[
            Submission]:
    log.debug(f"searching {subreddit_name} for '{query}' with sort '{sort}' and limit '{limit}'")
    submissions = []
    async with Reddit(
            client_id=os.getenv("REDDIT_ID"),
            client_secret=os.getenv("REDDIT_SECRET"),
            user_agent=os.getenv("REDDIT_AGENT")
    ) as reddit:
        subreddit = await reddit.subreddit(subreddit_name)
        search_result = subreddit.search(query, sort=sort, limit=limit)
        async for post in search_result:
            submissions.append(post)
    return submissions


async def async_search_manga(query: str) -> MangaChapter | None:
    log.debug(f"searching |{query}| on r/manga")
    unfiltered = await _async_search_subreddit(subreddit_name="manga", query=f"[disc] {query}")
    return _filter_post(query, unfiltered)


async def get_last_chapter_info(title: str) -> MangaChapter | None:
    log.debug(f"Fetching last chapter for {title}")

    try:
        fetched_chapter = await async_search_manga(title)
    except Exception as e:
        log.error(f"Error while searching for {title}: {e}")
        log.debug(f"Did not found: {title}")
        return None

    if not fetched_chapter:
        log.debug(f"Did not found: {title}")
        return None

    if not fetched_chapter.link:
        log.debug("Found new chapter but no link were provided")
    else:
        log.debug(f"Found chapter for: {title} n°{fetched_chapter.number}")

    return MangaChapter(manga_title=title, number=fetched_chapter.number, link=fetched_chapter.link)
