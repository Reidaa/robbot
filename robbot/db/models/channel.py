from uuid import UUID

from pony.orm import Required, Set, PrimaryKey

from . import db


class Channel(db.Entity):
    _table_ = 'channel'
    id = PrimaryKey(int, auto=True)
    mangas = Set('Manga')
    channel_id = Required(UUID, unique=True)
