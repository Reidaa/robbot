from asyncpraw.models import Submission

from src.helpers import get_chapter_number
from src.reddit.helpers import get_async_reddit


async def search_manga_posts(title: str) -> list:
    posts = []
    reddit = get_async_reddit()
    r_manga = await reddit.subreddit("manga")
    search_results = r_manga.search(
        query=f"[disc] {title}",
        sort="relevance"
    )
    async for post in search_results:
        posts.append(post)
    return posts


async def search_manga(title: str) -> dict | None:
    def filter_fun(x: Submission):
        title = x.title.lower()
        if "[disc]" in title and "chapter" in title:
            return x

    unfiltered = await search_manga_posts(title)
    results = list(filter(filter_fun, unfiltered))
    chapter_list = [get_chapter_number(submission.title) for submission in results]
    last_chapter = max(chapter_list)
    idx = chapter_list.index(last_chapter)
    return {
        "title": results[idx].title[7:],
        "chapter_number": last_chapter,
        "link": results[idx].url
    }
