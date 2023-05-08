import dotenv

dotenv.load_dotenv()

from robbot.db import database

database.erase()
database.create()
database.seed()
