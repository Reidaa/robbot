from services.mangaupdate.AsyncClient import client


async def search_mangas(title: str):
    response, error = await client.search_series(title, body_params={"type": "Manga"})

    if error:
        return None

    if response:
        return [
            {
                "series_id": result["record"]["series_id"],
                "title": result["record"]["title"]
            } for result in response.results
        ]

async def test():
    import logging

    logging.basicConfig(
        format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG
    )

    mangas = await search_mangas("Dragon Ball Z")

    if mangas:
        for manga in mangas:
            print(manga["title"], manga["series_id"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(test())
