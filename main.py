import os
import re
import asyncio

import discord
import asyncpraw
from dotenv import load_dotenv

load_dotenv()

from src.events import on_feur, on_quoi, on_citation
from src.helper import user_ping, role_ping


def is_test():
    return True if ("test" in ENV) else False


TOKEN = os.getenv("TOKEN")
LEANDRE = os.getenv("LEANDRE")
ENV = os.getenv("ENV")
REDDIT = {
    "CLIENT_ID": os.getenv("REDDIT_ID"),
    "CLIENT_SECRET": os.getenv("REDDIT_SECRET"),
    "USER_AGENT": os.getenv("REDDIT_AGENT")
}


def is_leandre(user: discord.Member):
    username = f"{user.name}#{user.discriminator}"
    if username == LEANDRE:
        return True
    else:
        return False

class MyBot(discord.Client):
    def __init__(self, *, gintents: discord.Intents):
        super().__init__(intents=gintents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        if is_test():
            # Synchronize the app commands to one guild.
            # Instead of specifying a guild to every command, we copy over our global commands instead.
            # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
            my_guild_id = int(os.getenv("MY_GUILD"))
            my_guild = discord.Object(id=my_guild_id)
            # This copies the global commands over to your guild.
            self.tree.copy_global_to(guild=my_guild)
            await self.tree.sync(guild=my_guild)

    async def on_ready(self):
        print('Logged on as', self.user)
        while True:
            await asyncio.sleep(60)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send(f'pong {user_ping(244703117659209728)}')
            return

        if message.content[-4:].lower() == "quoi" and is_leandre(message.author):
            return await on_quoi(message)

        if message.content.lower() == "feur" and is_leandre(message.author):
            return await on_feur(message)

        if re.match(r'^([A-Za-z]+):\s*', message.content):
            return await on_citation(message)


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.presences = True
intents.members = True
bot = MyBot(gintents=intents)


@bot.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")


@bot.tree.command()
@discord.app_commands.describe(
    whatever="whatever"
)
async def enable(interaction: discord.Interaction, whatever: str):
    print(interaction.message)
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")



@bot.tree.command()
async def reddit(interaction: discord.Interaction):
    reddit = asyncpraw.Reddit(
        client_id=REDDIT["CLIENT_ID"],
        client_secret=REDDIT["CLIENT_SECRET"],
        user_agent=REDDIT["USER_AGENT"]
    )
    r_manga = await reddit.subreddit("manga")
    submissions = r_manga.hot(limit=100)
    async for submission in submissions:
        if "[DISC] Chainsaw Man" in submission.title:
            result = submission.title

    await interaction.response.send_message(f"Done, {interaction.user.mention}, Chapters: {result}")


bot.run(os.getenv("TOKEN"))
