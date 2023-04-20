import asyncio
import os
from typing import Optional
import logging

import discord
from discord.ext import tasks

from robbot.t import Manga, SearchMangaResult, MangaChapter
from robbot.services.reddit import search_manga
from robbot import logger

SERIES = {
    "Chainsaw Man": Manga(
        title="Chainsaw Man",
        last_chapter=-1,
        roles_to_notify=[1087136295807099032, ],
    ),
    "My hero academia": Manga(
        title="My hero academia",
        last_chapter=-1,
        roles_to_notify=[1087136295807099032, ],
        users_to_notify=[209770215163035658, ],
    ),
    "jujutsu kaisen": Manga(
        title="jujutsu kaisen",
        last_chapter=-1,
        roles_to_notify=[],
        users_to_notify=[],
    ),
    "yumeochi": Manga(
        title="yumeochi",
        last_chapter=-1,
        roles_to_notify=[],
        users_to_notify=[],
    ),
    "dandadan": Manga(
        title="dandadan",
        last_chapter=-1,
        roles_to_notify=[],
        users_to_notify=[],
    ),
    "I Want to Be Praised by a Gal Gamer!": Manga(
        title="I Want to Be Praised by a Gal Gamer!",
        last_chapter=-1,
        roles_to_notify=[],
        users_to_notify=[],
    ),
}


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
                return await interaction.response.send_message(f"Only the owner can shutdown the bot")

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

        @self.tree.command()
        async def reset(interaction: discord.Interaction):
            for manga in SERIES.values():
                manga.last_chapter = -1
            return await interaction.response.send_message(f"Reset")


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
        await update_last_chapter()

        for channel_id in self.channels_id:
            self.channels.append(self.get_channel(int(channel_id)))

        self.notify_new_releases.start()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            logger.debug(f"Senging '{'pong'}' to {message.channel}")
            return await message.channel.send('pong')

    async def close(self):
        """Logs out of Discord"""
        self.notify_new_releases.cancel()
        await super().close()
        logger.info("Closed")

    async def shutdown(self):
        """
        Gracefully kill the Bot.
        To be called from commands
        """
        await self.close()

    @tasks.loop(seconds=60)
    async def notify_new_releases(self):
        logger.debug("Searching for submissions")

        for key in SERIES:
            chapter = await get_latest_chapter_info(title=key)
            if chapter:
                response = format_response(chapter)
                for channel in self.channels:
                    logger.debug(f"Sending |{response}| to channel |{channel.name}|")
                    await channel.send(response)
                SERIES[key].last_chapter = chapter.number

        logger.info("Finished searching for submissions")




async def get_latest_chapter_info(title: str) -> MangaChapter | None:
    try:
        manga = get_series(title)
    except KeyError:
        logger.debug(f"Did not found: {title}")
        return None

    try:
        result = await search_manga(title)
    except Exception as e:
        logger.error(f"Error while searching for {title}: {e}")
        return None

    if not result:
        logger.debug(f"Did not found: {title}")
        return None

    if result.chapter <= manga.last_chapter:
        logger.debug(f"No new chapters for: {title} (last chapter: {manga.last_chapter})")
        return None

    if not result.link:
        logger.debug("Found new chapter but no link were provided")
        return MangaChapter(title=title, number=result.chapter, link=None)

    logger.debug(f"Found new chapter for: {title} (last chapter: {manga.last_chapter})")
    return MangaChapter(title=title, number=result.chapter, link=result.link)


def get_series(title: str) -> Manga:
    m = SERIES.get(title)
    return m


def format_response(chapter: MangaChapter) -> str:
    if chapter.link:
        return f"{chapter.title} {chapter.number}: {chapter.link}"
    else:
        return f"A new chapter for {chapter.title} was found but no link were provided"

async def update_last_chapter():
    for key in SERIES:
        if SERIES[key].last_chapter == -1:
            result: SearchMangaResult = await search_manga(key)
            if result:
                SERIES[key].last_chapter = result.chapter - 1
