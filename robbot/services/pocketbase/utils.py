from robbot.services.pocketbase.AsyncClient import AsyncPocketBaseClient
from robbot.services.pocketbase.models import Manga, Channel, PocketbaseError, BackendError
from robbot import log


class AsyncPocketBaseUtils:
    def __init__(self, pb: AsyncPocketBaseClient):
        self.pb: AsyncPocketBaseClient = pb

    async def register_channel(self, channel_id: int) -> bool:
        try:
            await self.pb.collection("channels").get_first_list_item(filter=f"channel_id={channel_id}")
        except PocketbaseError:
            return False
        else:
            return True

    async def register_manga(self, title: str, last_chapter: int = -1, cover_url: str = None) -> bool:
        try:
            await self.pb.collection("mangas").create(
                body_params={
                    "name": title,
                    "last_chapter": last_chapter,
                    "cover_url": cover_url
                }
            )
        except PocketbaseError:
            return False
        else:
            return True

    async def is_channel_in_db(self, channel_id: int) -> bool:
        try:
            await self.pb.collection("channels").get_first_list_item(filter=f"channel_id={channel_id}")
        except PocketbaseError:
            return False

        return True

    async def is_manga_in_db(self, title: str) -> bool:
        try:
            await self.pb.collection("mangas").get_first_list_item(filter=f"name='{title.lower()}'")
        except PocketbaseError:
            return False
        else:
            return True

    async def is_manga_registered_on_channel(self, title: str, channel_id: int) -> bool:
        if not await self.is_channel_in_db(channel_id):
            return False
        if not await self.is_manga_in_db(title):
            return False

        try:
            channel_record = await self.pb.collection("channels").get_first_list_item(filter=f"channel_id={channel_id}",
                                                                                query_params={"expand": "mangas"})
        except PocketbaseError:
            return False

        for manga_record in channel_record.expand["mangas"]:
            if manga_record["name"] == title:
                return True

        return False

    async def add_manga_to_channel(self, title: str, channel_id: int):
        if not await self.is_channel_in_db(channel_id):
            raise BackendError("Channel not registered")

        if not await self.is_manga_in_db(title):
            raise BackendError("Manga not registered")

        try:
            manga_record = await self.pb.collection("mangas").get_first_list_item(filter=f"name='{title}'")
            channel_record = await self.pb.collection("channels").get_first_list_item(filter=f"channel_id={channel_id}")
            if manga_record.id in channel_record.fields["mangas"]:
                raise BackendError("Manga already registered on channel")
            await self.pb.collection("channels").update(
                id=channel_record.id,
                body_params={
                    "mangas": [*channel_record.fields["mangas"], manga_record.id]
                }
            )
        except PocketbaseError:
            return False

        return True

    async def get_manga(self, title: str) -> Manga | None:
        try:
            res = await self.pb.collection("mangas").get_first_list_item(filter=f"name='{title}'")
        except PocketbaseError:
            return None

        ret = Manga(
            id=res.id,
            name=res.fields["name"],
            last_chapter=res.fields["last_chapter"],
            cover_url=res.fields["cover_url"]
        )
        return ret

    async def get_channel(self, channel_id: int) -> Channel | None:
        try:
            res = await self.pb.collection("channels").get_first_list_item(filter=f"channel_id={channel_id}")
        except PocketbaseError:
            return None

        ret = Channel(id=res.id, channel_id=res.fields["channel_id"], manga_record_ids=res.fields["mangas"])
        return ret

    async def get_mangas_on_channel(self, channel_id: int) -> list[Manga] | None:
        """Get all mangas registered on a channel
        Raises:
            PocketbaseError:

        """
        mangas = []

        try:
            res = await self.pb.collection("channels").get_first_list_item(
                filter=f"channel_id={channel_id}",
                query_params={"expand": "mangas"}
            )
        except PocketbaseError:
            return None

        for manga_record in res.expand["mangas"]:
            mangas.append(Manga(
                id=manga_record["id"],
                name=manga_record["name"],
                last_chapter=manga_record["last_chapter"],
                cover_url=manga_record["cover_url"]
            ))
        return mangas

    async def get_all_mangas(self) -> list[Manga] | None:
        mangas = []

        try:
            res = await self.pb.collection("mangas").get_full_list()
        except PocketbaseError:
            return None

        for manga_record in res:
            mangas.append(Manga(
                id=manga_record["id"],
                name=manga_record["name"],
                last_chapter=manga_record["last_chapter"],
                cover_url=manga_record["cover_url"],
                channel_record_ids=manga_record["channels"]
            ))
        return mangas

    async def register_manga_on_channel(self, manga_title: str, channel_id: int, ) -> Channel | None:
        raise NotImplementedError

    async def remove_from_channel(self, channel_id: int, title: str) -> Channel | None:
        raise NotImplementedError

    async def update_manga(self, title: str, chapter: int) -> Manga | None:
        raise NotImplementedError


if __name__ == "__main__":
    import asyncio
    import logging
    from pprint import pprint

    record_id = "d435x41bnmn2iy5"
    title = "jujutsu kaisen"


    async def main():
        pb = AsyncPocketBaseClient(base_url="http://localhost:8080").start()
        utils = AsyncPocketBaseUtils(pb)

        logging.basicConfig(
            format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG
        )
        channel_record = await pb.collection("channels").get_one(record_id)
        print(await utils.is_channel_in_db(channel_record.fields["channel_id"]))

        await pb.stop()


    asyncio.run(main())
