import os

from dotenv import load_dotenv

load_dotenv()

from Bot import MyBot


def main():
    bot = MyBot()
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
