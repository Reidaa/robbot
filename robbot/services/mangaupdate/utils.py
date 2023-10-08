from services.mangaupdate.AsyncClient import client
from services.mangaupdate.models import SeriesRecord


async def get_mangas_option(title: str) -> list[dict[str, any]]:
    response = await client.search_series(
        title, body_params={"type": "Manga"}
    )

    if response:
        return [
            {
                "series_id": result["record"]["series_id"],
                "title": result["record"]["title"],
                "hit_title": result["record"]["hit_title"] if "hit_title" in result["record"].keys() else None,
                "description": result["record"]["description"],
                "year": result["record"]["year"],
                "image_url": result["record"]["image"]["url"],
            } for result in response.results
        ]


async def get_manga_info(series_id: str) -> SeriesRecord:
    return await client.get_series(series_id)


async def test():
    import logging

    logging.basicConfig(
        format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG
    )

    mangas = await get_mangas_option("Dragon Ball Z")

    if mangas:
        for manga in mangas:
            print(manga["title"], manga["series_id"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(test())
