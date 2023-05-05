from robbot.db.database import PonyDB
from robbot.t import MangaChapter

db = PonyDB()


def add_manga_to_channel(title: str, manga: MangaChapter, channel_id: int):
    if not db.manga.create(title=title, chapter=manga.number):
        raise Exception("Manga already exists")
    if not db.channel.update(channel_id, title):
        raise Exception("Could not update channel")
