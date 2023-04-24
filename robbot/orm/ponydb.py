import os
from uuid import UUID

from pony.orm import Database, Required, Set, PrimaryKey, db_session

from robbot.t import Manga

db = Database()


class DBChannel(db.Entity):
    _table_ = 'channel'
    id = PrimaryKey(int, auto=True)
    mangas = Set('DBManga')
    channel_id = Required(UUID, unique=True)


class DBManga(db.Entity):
    _table_ = 'manga'
    id = PrimaryKey(int, auto=True)
    title = Required(str, unique=True)
    last_chapter = Required(int, default="-1")
    channels = Set(DBChannel)


db.bind(provider="sqlite", filename="robbot.db", create_db=True)
db.generate_mapping(create_tables=True)


class DB:

    @staticmethod
    @db_session
    def get_channels_ids() -> list[UUID]:
        res = [channel.channel_id for channel in DBChannel.select()]
        return res

    @staticmethod
    @db_session
    def get_mangas_from_channel(channel_id: UUID) -> list[Manga]:
        res = [
            Manga(title=manga.title, last_chapter=manga.last_chapter)
            for manga in DBChannel.get(channel_id=channel_id).mangas.select()
        ]
        return res

    @staticmethod
    @db_session
    def get_manga_from_title(title: str) -> Manga:
        res = Manga(
            title=DBManga.get(title=title).title,
            last_chapter=DBManga.get(title=title).last_chapter,
        )
        return res

    @staticmethod
    @db_session
    def get_mangas() -> list[Manga]:
        res = [
            Manga(title=manga.title, last_chapter=manga.last_chapter)
            for manga in DBManga.select()
        ]
        return res

    @staticmethod
    @db_session
    def update_manga_chapter(title: str, chapter: int) -> bool:
        try:
            m = DBManga.get(title=title)
            m.last_chapter = chapter
        except Exception as e:
            return False
        finally:
            return True

    @staticmethod
    @db_session
    def seed():
        chainsaw = DBManga(title="chainsaw man", )
        mha = DBManga(title="my hero academia", )
        jujutsu = DBManga(title="jujutsu kaisen", )
        yumeochi = DBManga(title="yumeochi", )
        dandadan = DBManga(title="dandadan", )
        gal = DBManga(title="I Want to Be Praised by a Gal Gamer!", )

        if (testing_channel_id := os.getenv("TESTING_CHANNEL_ID")) is not None:
            test_channel = DBChannel(
                channel_id=testing_channel_id,
                mangas=[chainsaw, mha, yumeochi, dandadan, gal]
            )

        # Has no access to
        test_channel2 = DBChannel(
            channel_id=551475962273857548,
            mangas=[chainsaw, mha, jujutsu]
        )


if __name__ == "__main__":
    DB.seed()
