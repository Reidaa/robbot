from robbot.services.pocketbase.AsyncClient import AsyncPocketBaseClient


async def is_channel_registered(pb: AsyncPocketBaseClient, channel_id: int) -> bool:
    record, _ = await pb.collection("channels").get_first_list_item(filter=f"channel_id={channel_id}")
    return record is not None


async def is_manga_registered(pb: AsyncPocketBaseClient, title: str) -> bool:
    record, _ = await pb.collection("mangas").get_first_list_item(filter=f"name='{title.lower()}'")
    return record is not None


def is_manga_registered_on_channel(pb: AsyncPocketBaseClient, title: str, channel_id: int) -> bool:
    if not is_channel_registered(pb, channel_id):
        return False

    if not is_manga_registered(pb, title):
        return False

    channel_record, error = pb.collection("channels"). \
        get_first_list_item(filter=f"channel_id={channel_id}", query_params={"expand": "mangas"})

    if error:
        return False

    for manga_record in channel_record.expand["mangas"]:
        if manga_record["name"] == title:
            return True

    return False


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
        channel_record, _ = await pb.collection("channels").get_one(record_id)
        print(await is_channel_registered(pb, channel_record.fields["channel_id"]))

        await pb.stop()


    asyncio.run(main())
