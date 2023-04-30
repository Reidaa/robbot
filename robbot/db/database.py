from uuid import UUID

from pony import orm

from robbot.db.models import Channel as DBChannel
from robbot.db.models import Manga as DBManga
from robbot.db.models import db
from robbot.t import Manga

# db.bind(provider="sqlite", filename="robbot.db", create_db=True)
db.bind(
    provider='postgres',
    user="dev",
    password='root',
    host='localhost',
    database='robbot'
)

db.generate_mapping(create_tables=True)


class PonyDB:
    class manga:

        @staticmethod
        @orm.db_session()
        def unique(title: str) -> Manga | None:
            if obj := DBManga.get(title=title):
                return Manga(title=obj.title, last_chapter=obj.last_chapter)
            else:
                return None

        @staticmethod
        @orm.db_session()
        def many(channel_id: int | UUID) -> list[Manga]:
            return [
                Manga(title=i.title, last_chapter=i.last_chapter)
                for i in DBChannel.get(channel_id=channel_id).mangas.select()
            ]

        @staticmethod
        @orm.db_session()
        def all() -> list[Manga]:
            return [
                Manga(title=i.title, last_chapter=i.last_chapter)
                for i in DBManga.select()
            ]

        @staticmethod
        @orm.db_session()
        def update(title: str, last_chapter: int) -> bool:
            if obj := DBManga.get(title=title):
                obj.last_chapter = last_chapter
                return True
            else:
                return False

    class channel:

        @staticmethod
        @orm.db_session()
        def all() -> list[int]:
            return [i.channel_id for i in DBChannel.select()]

        @staticmethod
        @orm.db_session()
        def create(channel_id: int | UUID) -> bool:
            if r := DBChannel.get(channel_id=channel_id):
                return True
            else:
                return False


@orm.db_session
def seed():
    chainsaw = DBManga(title="chainsaw man", )
    mha = DBManga(title="my hero academia", )
    jujutsu = DBManga(title="jujutsu kaisen", )
    yumeochi = DBManga(title="yumeochi", )
    dandadan = DBManga(title="dandadan", )
    gal = DBManga(title="I Want to Be Praised by a Gal Gamer!", )

    test_channel = DBChannel(
        channel_id=1082820333477838868,
        mangas=[chainsaw, mha, yumeochi, dandadan, gal]
    )

    # Has no access to
    test_channel2 = DBChannel(
        channel_id=551475962273857548,
        mangas=[chainsaw, mha, jujutsu]
    )


if __name__ == "__main__":
    seed()
