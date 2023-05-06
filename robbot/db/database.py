from uuid import UUID

from pony import orm

from robbot.db.models import Channel as DBChannel
from robbot.db.models import Manga as DBManga
from robbot.db.models import db
from robbot.t import Manga, Channel

db.bind(provider="sqlite", filename="robbot.db", create_db=True)
db.generate_mapping(create_tables=True)


class PonyDB:
    class manga:

        @staticmethod
        @orm.db_session()
        def unique(title: str) -> Manga | None:
            if m := DBManga.get(title=title.lower()):
                return Manga(title=m.title, last_chapter=m.last_chapter)
            else:
                return None

        @staticmethod
        @orm.db_session()
        def many(channel_id: int) -> list[Manga]:
            if c := DBChannel.get(channel_id=str(channel_id)):
                return [
                    Manga(title=i.title, last_chapter=i.last_chapter)
                    for i in c.mangas.select()
                ]
            else:
                return []

        @staticmethod
        @orm.db_session()
        def all() -> list[Manga]:
            return [
                Manga(title=i.title, last_chapter=i.last_chapter)
                for i in DBManga.select()
            ]

        @staticmethod
        @orm.db_session()
        def update(title: str, last_chapter: int) -> Manga | None:
            if manga := DBManga.get(title=title.lower()):
                manga.last_chapter = last_chapter
                return Manga(title=manga.title, last_chapter=manga.last_chapter)
            else:
                return None

        @staticmethod
        @orm.db_session()
        def create(title: str, chapter: int = -1) -> Manga | None:
            if manga := DBManga(title=title.lower(), last_chapter=chapter):
                return Manga(title=manga.title, last_chapter=manga.last_chapter)
            else:
                return None

    class channel:

        @staticmethod
        @orm.db_session()
        def all() -> list[int]:
            return [int(c.channel_id) for c in DBChannel.select()]

        @staticmethod
        @orm.db_session()
        def create(channel_id: int | UUID) -> Channel | None:
            if c := DBChannel(channel_id=str(channel_id)):
                return Channel(channel_id=int(c.channel_id))
            else:
                return None

        @staticmethod
        @orm.db_session()
        def update(channel_id: int, title: str) -> Channel | None:
            if c := DBChannel.get(channel_id=str(channel_id)):
                if m := DBManga.get(title=title.lower()):
                    c.mangas.add(m)
                    return Channel(
                        channel_id=int(c.channel_id),
                        mangas=[Manga(title=i.title, last_chapter=i.last_chapter) for i in c.mangas.select()]
                    )
                else:
                    return None
            else:
                return None

        @staticmethod
        @orm.db_session()
        def remove(channel_id: int, title: str) -> Channel | None:
            if c := DBChannel.get(channel_id=str(channel_id)):
                if m := DBManga.get(title=title.lower()):
                    c.mangas.remove(m)
                    return Channel(
                        channel_id=int(c.channel_id),
                        mangas=[Manga(title=i.title, last_chapter=i.last_chapter) for i in c.mangas.select()]
                    )
                else:
                    return None
            else:
                return None

        @staticmethod
        @orm.db_session()
        def unique(channel_id: int) -> Channel | None:
            if c := DBChannel.get(channel_id=str(channel_id)):
                return Channel(
                    channel_id=int(c.channel_id),
                    mangas=[Manga(title=i.title, last_chapter=i.last_chapter) for i in c.mangas.select()]
                )
            else:
                return None


def reset_db():
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    seed()


@orm.db_session()
def seed():
    chainsaw = DBManga(title="chainsaw man", )
    mha = DBManga(title="my hero academia", )
    jujutsu = DBManga(title="jujutsu kaisen", )
    yumeochi = DBManga(title="yumeochi", )
    dandadan = DBManga(title="dandadan", )
    gal = DBManga(title="I Want to Be Praised by a Gal Gamer!".lower(), )

    DBChannel(
        channel_id=str(1082820333477838868),
        mangas=[chainsaw, mha, yumeochi, dandadan, gal]
    )

    # Has no access to
    DBChannel(
        channel_id=str(551475962273857548),
        mangas=[chainsaw, mha, jujutsu]
    )


if __name__ == "__main__":
    reset_db()
