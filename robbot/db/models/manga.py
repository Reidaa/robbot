from pony.orm import Required, Set, PrimaryKey

from . import db


class Manga(db.Entity):
    _table_ = 'Manga'
    id = PrimaryKey(int, auto=True)
    title = Required(str, unique=True)
    last_chapter = Required(int, default="-1")
    channels = Set("Channel")
