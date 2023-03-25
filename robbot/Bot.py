import asyncio
import os

import discord

from robbot.RedditClient import search_manga
from robbot import logger
from robbot.utils import role_ping

SERIES = {
    "Chainsaw Man": {
        "last_chapter": 123,
        "roles": [1087136295807099032, ],
        "users": []
    }
}


class Bot(discord.Client):
    def __init__(self):

        self.channels_id = []
        if (testing_channel_id := os.getenv("TESTING_CHANNEL_ID")) is not None:
            self.channels_id.append(testing_channel_id)

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True

        super().__init__(intents=intents)
        self.tree: discord.app_commands.CommandTree | None = None

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
            result = await search_manga(title)

            if result:
                await interaction.response.send_message(f"{result['title']}: {result['link']}")
            else:
                await interaction.response.send_message(f"Did not found the manga {interaction.user.mention}")

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

    async def on_ready(self):
        logger.info('Logged on as', self.user)
        # while True:
        #     await search_submissions(self)
        #     await asyncio.sleep(60)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            logger.debug(f"Senging '{'pong'}' to {message.channel}")
            return await message.channel.send('pong')
            # return await send_message(message.channel, "pong")

    async def close(self):
        """Logs out of Discord"""
        await super().close()
        logger.info("Closed")

    async def shutdown(self):
        """ Gracefully kill the Bot.
        To be called from commands
        """
        await self.close()


async def search_submissions(bot: Bot):
    logger.debug("Searching for submissions")
    for series in SERIES:
        t = await find_new_chapters(series)
        for channel_id in bot.channels_id:
            channel = bot.get_channel(int(channel_id))
            if t:
                await send_message(channel, t)
    # t = await find_new_chapters("chainsaw")
    # for channel_id in CHANNELS:
    #     channel = bot.get_channel(int(channel_id))
    #     await channel.send("Weeb Testing, next test in 60 seconds")
    #     await channel.send(t)

async def send_message(channel: discord.channel , message: str):
    logger.debug(f"Senging '{t}' to {channel.name}")
    return await channel.send(message)


async def find_new_chapters(title: str) -> str | None:
    result = await search_manga(title)

    if result:
        if result['chapter'] > SERIES[title]['last_chapter']:
            logger.debug(f"Found new chapter for: {title}")
            response = f"{title} {result['chapter']}: {result['link']} {role_ping(SERIES[title]['roles'][0])}"
        else:
            logger.debug(f"No new chapters for: {title} (last chapter: {SERIES[title]['last_chapter']})")
            response = None
    else:
        logger.debug(f"Did not found: {title}")
        response = None

    logger.debug(f"response is: {response}")
    return response
