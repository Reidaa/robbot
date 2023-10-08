import httpx

from robbot.services.anilist.models import AnilistError

BASE_URL = "https://graphql.anilist.co"

async def send_query(query: str, variables: dict[str, any] | None = None):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/", json={"query": query, "variables": variables})

    response_dict = response.json()

    match response.status_code:
        case 200:
            return response_dict["data"]
        case _:
            raise AnilistError("Anilist API Error", response_dict["errors"])
