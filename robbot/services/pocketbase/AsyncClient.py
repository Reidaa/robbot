import httpx

from robbot.services.pocketbase.models import ListResult, Error, RecordResponse


class AsyncCollection:
    def __init__(self, client: httpx.AsyncClient, collection_name: str):
        self._client = client
        self._collection_name = collection_name

    async def get_list(self, page: int = 1, per_page: int = 30, query_params: dict | None = None) -> tuple[
        ListResult | None, Error | None]:
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
                return ListResult(**response_dict), None
            case _:
                return None, Error(**response_dict)

    async def get_full_list(self, per_page: int = 200, query_params: dict | None = None) -> tuple[
        list[RecordResponse] | None, Error | None]:
        raise NotImplementedError

    async def get_first_list_item(self, filter: str, query_params: dict = None) -> tuple[
        RecordResponse | None, Error | None]:
        if query_params is None:
            query_params = {}
        response, error = await self.get_list(1, 1, query_params={"filter": filter, **query_params})
        if error:
            return None, error
        if len(response.items) == 0:
            return None, Error(code=404, message="The requested resource wasn't found.", data={})
        return RecordResponse(**response.items[0]), None

    async def get_one(self, id: str, query_params: dict = None) -> tuple[RecordResponse | None, Error | None]:
        if query_params is None:
            query_params = {}

        response = await self._client.get(
            f"/api/collections/{self._collection_name}/records/{id}",
            params=query_params
        )

        response_dict = response.json()

        match response.status_code:
            case 200:
                return RecordResponse(**response_dict), None
            case _:
                return None, Error(**response_dict)

    async def create(self, body_params: dict = None, query_params: dict = None) -> tuple[
        RecordResponse | None, Error | None]:
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
                return RecordResponse(**response_dict), None
            case _:
                return None, Error(**response_dict)

    async def update(self, id: str, body_params: dict = None, query_params: dict = None) -> tuple[
        RecordResponse | None, Error | None]:

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
                return RecordResponse(**response_dict), None
            case _:
                return None, Error(**response_dict)

    async def delete(self, id: str, query_params: dict = None) -> tuple[bool, Error | None]:
        if query_params is None:
            query_params = {}

        response = await self._client.delete(
            f"/api/collections/{self._collection_name}/records/{id}",
            params=query_params
        )

        match response.status_code:
            case 204:
                return True, None
            case _:
                return False, Error(**response.json())


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

    record_id = "d435x41bnmn2iy5"
    title = "jujutsu kaisen"


    async def main():

        pb = AsyncPocketBaseClient(base_url="http://localhost:8080").start()

        logging.basicConfig(
            format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG
        )
        # response, error = await pb.collection("channels").get_one(record_id, query_params={"expand": "mangas"})
        #
        # if error:
        #     pprint(error)
        #
        # if response:
        #     pprint(response)

        channel_record, error = await pb.collection("channels"). \
            get_first_list_item(filter=f"channel_id={1082820333477838800}", query_params={"expand": "mangas"})

        if error:
            print(False)

        for manga_record in channel_record.expand["mangas"]:
            if manga_record["name"] == title:
                print(True)

        await pb.stop()


    asyncio.run(main())
