from pony import orm
import os

db = orm.Database()


class Manga(db.Entity):
    name = orm.Required(str, unique=True)
    last_chapter = orm.Required(int)

class Citation(db.Entity):
    author = orm.Required(str)
    who = orm.Required(str)
    content = orm.Required(str)
    time = orm.Required(int)



db.bind(
    provider="postgres",
    user='root',
    password='root',
    host='localhost',
    database='docker'
)


orm.set_sql_debug(True)
# db.bind(
#     provider="sqlite",
#     filename="database.sqlite",
#     create_db=True
# )

db.generate_mapping(create_tables=True)



@orm.db_session
def create_manga(name: str, last_chapter: int = 0):
    Manga(name=name, last_chapter=last_chapter)

@orm.db_session
def read_manga(name: str):
    manga = Manga.get(name=name)
    return {
        "name": manga.name,
        "chapter": manga.last_chapter
    }

@orm.db_session
def update_manga(name: str, last_chapter: int):
    manga = Manga.get(name=name)
    manga.last_chapter = last_chapter
    orm.commit()
    return {
        "name": manga.name,
        "chapter": manga.last_chapter
    }

@orm.db_session
def delete_manga(name: str):
    manga = Manga.get(name=name)
    try:
        Manga[manga.id].delete()
        orm.commit()
    except AttributeError as err:
        return False
    except Exception as err:
        raise err
    finally:
        return True