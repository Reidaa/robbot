from robbot.db.database import PonyDB
from robbot.t import S_MangaChapter, S_Manga, S_Channel

db = PonyDB()


def add_manga_to_channel(title: str, manga: S_MangaChapter, channel_id: int):
    if not db.manga.create(title=title, chapter=manga.number):
        raise Exception("Manga already exists")
    if not db.channel.add(channel_id, title):
        raise Exception("Could not update channel")


def is_channel_registered(channel_id: int) -> bool:
    return db.channel.unique(channel_id=channel_id) is not None


def create_channel(channel_id: int) -> None:
    if not db.channel.create(channel_id):
        raise Exception("Could not create channel")


def get_channel(channel_id: int) -> S_Channel | None:
    return db.channel.unique(channel_id=channel_id)


def get_all_channels_id() -> list[int]:
    return db.channel.all()


def get_mangas_on_channel(channel_id: int) -> list[S_Manga]:
    if not is_channel_registered(channel_id):
        raise Exception("Channel is not registered")
    return db.manga.many(channel_id=channel_id)


def get_manga(title: str) -> S_Manga | None:
    return db.manga.unique(title=title)


def add_to_channel(channel_id: int, title: str) -> S_Channel | None:
    return db.channel.add(channel_id=channel_id, title=title)


def remove_from_channel(channel_id: int, title: str) -> S_Channel | None:
    return db.channel.remove(channel_id=channel_id, title=title)


def update_manga(title: str, chapter: int) -> S_Manga | None:
    return db.manga.update(title=title, last_chapter=chapter)
