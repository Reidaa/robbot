import os
import re
import asyncio

import discord
from discord import app_commands
from dotenv import load_dotenv

from events import on_feur, on_quoi, on_citation


load_dotenv()

channels = {

}

MY_GUILD = discord.Object(id=int(os.getenv("MY_GUILD")))


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
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    async def on_ready(self):
        print('Logged on as', self.user)

        while True:
            await asyncio.sleep(60)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
            return

        if message.content[-4:].lower() == "quoi":
            return await on_quoi(message)

        if message.content.lower() == "feur":
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

bot.run(os.getenv("TOKEN"))
