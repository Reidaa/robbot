import os

import discord
from discord.ext import commands, tasks

from robbot import log
from robbot.services.pocketbase.AsyncClient import AsyncPocketBaseClient
from robbot.services.pocketbase.utils import AsyncPocketBaseUtils
from robbot.services.mangaupdate.utils import get_mangas_option
from robbot.bot.views.SearchMangaView import SearchMangaView
from robbot.bot.Embeds import ErrorEmbed

guilds_ids: list | None = []

if t := os.getenv("TESTING_GUILD_ID"):
    guilds_ids.append(t)
else:
    guilds_ids = None

PB_URL = os.getenv("PB_URL", "http://localhost:8080")


class Manga(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._pb = AsyncPocketBaseClient(PB_URL)
        self._pb_utils = AsyncPocketBaseUtils(self._pb)

        self._pb.start()
        # self.notify_new_releases.start()

    @tasks.loop(minutes=5)
    async def notify_new_releases(self):
        log.debug("Searching for releases...")

        # for all_mangas in db.get_all_mangas():
        #      if manga.new_rleases is True:
        #         for channel in manga.channels:
        #             await channel.send(manga.new_releases)

        # for channel_id in get_all_channels_id():
        #     channel = self.bot.get_channel(channel_id)
        #     if not channel:
        #         log.warning(f"channel {channel_id} not found")
        #         continue
        #     releases = []
        #     for manga in get_mangas_on_channel(channel_id=channel_id):
        #         chapter = await get_new_chapter_info(manga.title)
        #         if chapter:
        #             releases.append(format_response(chapter))
        #             update_manga(manga.title, chapter.number)
        #     for release in releases:
        #         await channel.send(release)

        log.info("Finished searching for releases")

    @discord.slash_command(description="Find the latest chapter for a given manga", guild_ids=guilds_ids)
    @discord.option("title", type=str, description="The title of the manga to search for", required=True)
    async def search(self, ctx: discord.ApplicationContext, title: str):
        await ctx.defer()

        manga_options = await get_mangas_option(title)
        if len(manga_options) == 0:
            return await ctx.respond(embed=ErrorEmbed(f"Did not find anything for: __{title}__"))

        view = SearchMangaView(manga_options)
        response = await ctx.respond(content="Select a manga", view=view)

        await view.wait()

        if not view.select.finished:
            return await response.edit(content=None, embed=ErrorEmbed("Timeout"), view=None)

    @discord.slash_command(description="Setup the bot for this channel", guild_ids=guilds_ids)
    @discord.option("channel", type=discord.TextChannel, description="The channel to setup the bot for", )
    async def setup(self, ctx: discord.ApplicationContext, channel: discord.TextChannel | None = None):
        channel = channel if channel else ctx.channel
        channel_info = self._pb_utils.get_channel(channel.id)

        if channel_info is None:
            await self._pb_utils.register_channel(channel.id)
            return await ctx.respond(f"Setup done for {channel.mention}")

        if channel_info is not None:
            return await ctx.respond(f"Setup already done for {channel.mention}")

    @discord.slash_command(
        description="Display the list of mangas registered on this channel",
        guild_ids=guilds_ids
    )
    @discord.option("channel", type=discord.TextChannel, description="The channel to display the queue for", )
    async def queue(self, ctx: discord.ApplicationContext, channel: discord.TextChannel | None = None):
        channel: discord.TextChannel = channel if channel else ctx.channel

        if not await self._pb_utils.is_channel_in_db(channel.id):
            return await ctx.respond(f"{channel.mention} is not registered !", ephemeral=True)

        try:
            mangas = await self._pb_utils.get_mangas_on_channel(channel.id)
        except Exception as e:
            return await ctx.respond(f"Error: {e}", ephemeral=True)

        embed = discord.Embed(title=f"{channel.mention}'s tracked manga", color=discord.Color.blurple())

        if len(mangas) > 0:
            response = [f"**{manga.name}**: {manga.last_chapter}" for manga in mangas]
            embed.add_field(name="", value="\n".join(response), inline=True)
            return await ctx.respond(embed=embed)
        else:
            embed.description = "Nothing registered"
            return await ctx.respond(embed=embed)

    @discord.slash_command(
        name="register",
        description="Register a manga to receive notifications when a new chapter is released",
        guild_ids=guilds_ids
    )
    @discord.option("channel", type=discord.TextChannel, description="The channel to register the manga on",
                    required=True)
    @discord.option("title", type=str, description="The title of the manga to search for", required=True)
    async def register_manga_on_channel(self,
                                        ctx: discord.commands.context.ApplicationContext,
                                        channel: discord.TextChannel,
                                        title: str):
        raise NotImplementedError
        # await ctx.defer()
        #
        # channel: discord.TextChannel = channel if channel else ctx.channel
        #
        # if not await self._pb_utils.is_channel_in_db(channel.id):
        #     return await ctx.followup.send(f"Please use /setup on {channel.mention} first", ephemeral=True)
        #
        # if await self._pb_utils.is_manga_registered_on_channel(channel_id=channel.id, title=title):
        #     return await ctx.followup.send(f"**{title}** is already registered")
        #
        # if await self._pb_utils.is_manga_in_db(title=title):
        #     if await self._pb_utils.register_manga_on_channel(channel_id=channel.id, manga_title=title):
        #         return await ctx.followup.send(f"Registered **{title}** on {channel.mention}")
        #     else:
        #         return await ctx.followup.send(f"Error", ephemeral=True)
        #
        # manga_options = await get_mangas_option(title)
        #
        # if len(manga_options) < 0:
        #     return await ctx.followup.send(f"Did not find anything for: {title}", ephemeral=True)
        #
        # manga_select = SelectMangaView(options=manga_options)
        #
        # search = await ctx.followup.send("f", view=manga_select)
        # await manga_select.wait()
        #
        # if manga_select.select.finish is None:
        #     return await search.edit(content="Canceled", view=None)
        # else:
        #     return await search.edit(content="T", view=None)

        # found_chapter = await async_search_manga(title)
        # if found_chapter:
        #     manga_select = SelectMangaView(title=title)
        #     search = await ctx.followup.send("f", view=manga_select)
        #     await manga_select.wait()
        #     return await ctx.followup.send(
        #         f"{found_chapter.manga_title}\n{found_chapter.link}, is this correct ?",
        #         view=RegisterMangaOnChannelView(author=ctx.author, title=title, pb_utils=self._pb_utils, )
        #     )
        # return await search.edit(content=f"Did not found **{title}**", view=None)

    @discord.slash_command(
        description="Unregister a manga to stop receiving notifications when a new chapter is released",
        guild_ids=guilds_ids, name="unregister")
    @discord.option(
        name="title", type=str, required=True,
        description="The REGISTERED title of the manga to remove", )
    @discord.option(
        name="channel", type=discord.TextChannel, required=True,
        description="The channel to unregister the manga from",
    )
    async def unregister(self,
                         ctx: discord.commands.context.ApplicationContext,
                         channel: discord.TextChannel,
                         title: str):
        await ctx.defer()

        channel: discord.TextChannel = channel if channel else ctx.channel

        if channel.guild != ctx.guild:
            return await ctx.followup.send("This channel is not from this server", ephemeral=True)

        if not self._pb_utils.is_channel_in_db(channel.id):
            return await ctx.followup.send(f"Please use /setup on {channel.mention} first", ephemeral=True)

        if not (self._pb_utils.get_manga(title=title)):
            return await ctx.followup.send(f"**{title}** is unregistered on {channel.mention}")

        if self._pb_utils.remove_from_channel(channel_id=channel.id, title=title):
            return await ctx.followup.send(f"Removed **{title}** from {channel.mention}")

        return await ctx.followup.send("Error", ephemeral=True)


def setup(bot):
    bot.add_cog(Manga(bot))
