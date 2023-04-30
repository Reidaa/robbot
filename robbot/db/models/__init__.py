from pony import orm

db = orm.Database()

from .channel import Channel
from .manga import Manga
