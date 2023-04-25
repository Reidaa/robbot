import logging
import os

import discord
from discord.ext import tasks

from robbot import logger
from robbot.db.ponydb import DB
from robbot.services.reddit import search_manga
from robbot.t import SearchMangaResult
from robbot.utils import update_last_chapter, format_response, get_new_chapter_info


class Bot(discord.Client):
    def __init__(self):
        self.tree: discord.app_commands.CommandTree | None = None

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True

        super().__init__(intents=intents)

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
        async def search(interaction: discord.Interaction, title: str):
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
        await update_last_chapter()
        self.notify_new_releases.start()

    async def close(self):
        """Logs out of Discord"""
        self.notify_new_releases.cancel()
        await super().close()
        logger.info("Closed")

    @tasks.loop(seconds=5 * 60)
    async def notify_new_releases(self):
        logger.debug("Searching for releases...")

        for channel_id in DB.get_channels_ids():
            channel = self.get_channel(int(channel_id))
            if not channel:
                logger.warning(f"channel {int(channel_id)} not found")
                continue
            releases = []
            for manga in DB.get_mangas_from_channel(channel_id):
                chapter = await get_new_chapter_info(manga.title)
                if chapter:
                    releases.append(format_response(chapter))
                    DB.update_manga_chapter(manga.title, chapter.number)
            for release in releases:
                await channel.send(release)

        logger.info("Finished searching for releases")

