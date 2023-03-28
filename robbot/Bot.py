import asyncio
import os
from typing import Optional
import logging

import discord

from robbot.types import Manga, SearchMangaResult
from robbot.services.reddit import search_manga
from robbot.services.db import get_mangas, update_chapter, get_manga
from robbot import logger
from robbot.utils import role_ping


class Bot(discord.Client):
    def __init__(self):

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True

        super().__init__(intents=intents)
        
        self.channels_id = []
        if (testing_channel_id := os.getenv("TESTING_CHANNEL_ID")) is not None:
            self.channels_id.append(testing_channel_id)


        self.tree: discord.app_commands.CommandTree | None = None
        self.channels: list[discord.channel] = []

        self.register_cmds()

    def register_cmds(self):
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of disc.Client, the bot will
        # maintain its own tree instead.
        self.tree = discord.app_commands.CommandTree(self)

        @self.tree.command()
        async def ping(interaction: discord.Interaction):
            await interaction.response.send_message(f"pong {interaction.user.mention}")

        @self.tree.command()
        async def shutdown(interaction: discord.Interaction):
            if interaction.user.id == 244703117659209728:
                await interaction.response.send_message(f"Shutting down...")
                await self.shutdown()
            else:
                return await interaction.response.send_message(f"t ki?")

        @self.tree.command()
        @discord.app_commands.describe(
            title="Title of the manga"
        )
        async def manga(interaction: discord.Interaction, title: str):
            response = f"Did not found the manga {interaction.user.mention}"
            result: SearchMangaResult = await search_manga(title)

            if result:
               response = f"Found {result.title} {result.chapter} {result.link}"
            
            return await interaction.response.send_message(response)

    async def setup_hook(self):
        if (testing_guild_id := os.getenv("TESTING_GUILD_ID")) is not None:
            logger.debug("Syncing commands with testing guild")
            # Synchronize the app commands to one guild.
            # Instead of specifying a guild to every command, we copy over our global commands instead.
            # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
            testing_guild = discord.Object(id=int(testing_guild_id))
            # This copies the global commands over to your guild.
            self.tree.copy_global_to(guild=testing_guild)
            await self.tree.sync(guild=testing_guild)

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        discord.utils.setup_logging(level=logging.INFO)
        return await super().start(token)

    async def on_ready(self):
        logger.info('Logged on as', self.user)
        
        for channel_id in self.channels_id:
            self.channels.append(self.get_channel(int(channel_id)))
        
        while True:
            message = await new_release(self)
            logger.info("waking up in 60")
            await asyncio.sleep(60)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            logger.debug(f"Senging '{'pong'}' to {message.channel}")
            return await message.channel.send('pong')

    async def close(self):
        """Logs out of Discord"""
        await super().close()
        logger.info("Closed")

    async def shutdown(self):
        """ Gracefully kill the Bot.
        To be called from commands
        """
        await self.close()

    async def spread(message: str):
        for channel in self.channels:
            logger.debug(f"Sending |{response}| to channel |{channel.name}|")
            await channel.send(message)


async def new_release(bot: Bot):
    logger.debug("Searching for submissions")
    
    with DBContext() as db:
        mangas = db.get_mangas()
    
    for key in mangas:
        response = await find_new_release(mangas[key])
        if response:
            bot.spread(response)
            with DBContext() as db:
                db.update_chapter(title=key, chapter=manga[key].last_chapter + 1)

    return

async def find_new_release(manga: Manga) -> Optional[str]:
    response: Optional[str] = None
    result: SearchMangaResult = await search_manga(manga.title)

    if result:
        if result.chapter > manga.last_chapter:
            if result.link:
                logger.debug(f"Found new chapter for: {manga.title} (last chapter: {manga.last_chapter})")
                response = f"{manga.title} {result.chapter}: {result.link}"
            else:
                logger.debug("Found new chapter but no link were provided")
                response = f"A new chapter for {manga.title} was found but no link were provided"
        else:
            logger.debug(f"No new chapters for: {manga.title} (last chapter: {manga.last_chapter})")
    else:
        logger.debug(f"Did not found: {manga.title}")

    return response
