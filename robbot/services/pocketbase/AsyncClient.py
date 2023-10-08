import httpx

from robbot.services.pocketbase.models import ListResult, RecordResponse, PocketbaseError


class AsyncCollection:
    def __init__(self, client: httpx.AsyncClient, collection_name: str):
        self._client = client
        self._collection_name = collection_name

    async def get_list(self, page: int = 1, per_page: int = 30, query_params: dict | None = None) -> ListResult:
        if query_params is None:
            query_params = {}

        response = await self._client.get(
            f"/api/collections/{self._collection_name}/records",
            params={
                "page": page,
                "per_page": per_page,
                **query_params
            }
        )

        response_dict = response.json()

        match response.status_code:
            case 200:
                return ListResult(**response_dict)
            case _:
                raise PocketbaseError(**response_dict)

    async def get_full_list(self, per_page: int = 200, query_params: dict | None = None) -> list[RecordResponse]:
        """Get all records from the collection.

        Raises:
            PocketbaseError: If the request fails.
        """
        if query_params is None:
            query_params = {}

        result = []

        async def request(page: int):
            response = await self.get_list(page, per_page, query_params)
            items = response.items
            total_items = response.totalItems

            result.extend(items)

            if len(items) and total_items > len(result):
                return await request(page + 1)

            return result

        return await request(1)

    async def get_first_list_item(self, filter: str, query_params: dict = None) -> RecordResponse:
        if query_params is None:
            query_params = {}
        response = await self.get_list(1, 1, query_params={"filter": filter, **query_params})
        if len(response.items) == 0:
            raise PocketbaseError(code=404, message="The requested resource wasn't found.", data={})
        return RecordResponse(**response.items[0])

    async def get_one(self, id: str, query_params: dict = None) -> RecordResponse:
        if query_params is None:
            query_params = {}

        response = await self._client.get(
            f"/api/collections/{self._collection_name}/records/{id}",
            params=query_params
        )

        response_dict = response.json()

        match response.status_code:
            case 200:
                return RecordResponse(**response_dict)
            case _:
                raise PocketbaseError(**response_dict)

    async def create(self, body_params: dict = None, query_params: dict = None) -> RecordResponse:
        if query_params is None:
            query_params = {}
        if body_params is None:
            body_params = {}

        response = await self._client.post(
            f"/api/collections/{self._collection_name}/records",
            json=body_params,
            params=query_params
        )

        response_dict = response.json()

        match response.status_code:
            case 200:
                return RecordResponse(**response_dict)
            case _:
                raise PocketbaseError(**response_dict)

    async def update(self, id: str, body_params: dict = None, query_params: dict = None) -> RecordResponse:
        """Updates a record.

        Args:
            id: The id of the record to update.
            body_params: The new values for the record. Defaults to None.
            query_params: The query parameters. Defaults to None.

        Return:
            RecordResponse: The updated record.

        Raises:
            PocketbaseError: If the request failed.
        """

        if query_params is None:
            query_params = {}
        if body_params is None:
            body_params = {}

        response = await self._client.patch(
            f"/api/collections/{self._collection_name}/records/{id}",
            json=body_params,
            params=query_params
        )

        response_dict = response.json()

        match response.status_code:
            case 200:
                return RecordResponse(**response_dict)
            case _:
                raise PocketbaseError(**response_dict)

    async def delete(self, id: str, query_params: dict = None) -> bool:
        if query_params is None:
            query_params = {}

        response = await self._client.delete(
            f"/api/collections/{self._collection_name}/records/{id}",
            params=query_params
        )

        match response.status_code:
            case 204:
                return True
            case _:
                raise PocketbaseError(**response.json())


class AsyncPocketBaseClient:

    def __init__(self, base_url: str):
        self._base_url = base_url
        self.collections = AsyncCollection
        self._async_client = None

    def collection(self, collection_name: str):
        if self._async_client is None:
            raise ValueError("Client not started yet")
        return self.collections(collection_name=collection_name, client=self._async_client)

    def start(self):
        self._async_client = httpx.AsyncClient(base_url=self._base_url)
        return self

    async def stop(self):
        await self._async_client.aclose()


if __name__ == "__main__":
    import asyncio
    import logging
    from pprint import pprint


    async def main():
        pb = AsyncPocketBaseClient(base_url="http://localhost:8080").start()

        logging.basicConfig(
            format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG
        )

        async def test():
            result = await pb.collection("mangas").get_full_list()
            return result

        channel_id = "1082820333477838800"
        title = "chainsaw man"

        pprint(await test())

        await pb.stop()


    asyncio.run(main())
