import asyncio
import os

import discord

from src.helpers import is_testing
from src.reddit import manga

CHANNELS = [
    "1082820297876574242",
]

SERIES = {
    "Chainsaw Man": {
        "chapters": 122,
        "roles": [1077695451148599398, ],
        "users": [""]
    }
}


class MyBot(discord.Client):
    def __init__(self, *, gintents: discord.Intents):
        super().__init__(intents=gintents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of disc.Client, the bot will
        # maintain its own tree instead.
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        if is_testing():
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
            t = await find_new_chapters("chainsaw")
            for channel_id in CHANNELS:
                channel = self.get_channel(int(channel_id))
                await channel.send("Weeb Testing, next test in 60 seconds")
                await channel.send(t)
            await asyncio.sleep(60)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            return await message.channel.send('pong')


async def find_new_chapters(title: str) -> str | None:
    result = await manga.search_manga(title)
    if result:
        return f"{result['title']}: {result['link']}"
    else:
        return f"Did not found {title}"
