import asyncio
import os
import re

import discord

from src.disc.events import is_feur, is_quoi, is_leandre, on_quoi, on_citation, on_feur
from src.helpers import is_testing, is_citation


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
            await asyncio.sleep(60)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            return await message.channel.send('pong')

        if is_leandre(message.author) and is_quoi(message.content):
            return await on_quoi(message)

        if is_leandre(message.author) and is_feur(message.content):
            return await on_feur(message)

        if is_citation(message.content):
            return await on_citation(message)
