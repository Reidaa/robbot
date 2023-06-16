import dotenv

dotenv.load_dotenv()

from robbot.db import database

print("Erasing database...")
database.erase()
print("Creating database...")
database.create()
print("Seeding database...")
database.seed()
print("Done!")
