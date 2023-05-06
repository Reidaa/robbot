from pony.orm import Required, Set, PrimaryKey

from . import db


class Channel(db.Entity):
    _table_ = 'Channel'
    id = PrimaryKey(int, auto=True)
    mangas = Set('Manga')
    channel_id = Required(str, unique=True)
