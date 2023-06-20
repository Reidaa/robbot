import os

import discord
from discord.ext import commands, tasks

from robbot import log
from robbot.services import database
from robbot.services import reddit
from robbot.t import S_MangaChapter
from robbot.utils import format_response
from services.database import is_channel_registered, get_channel, create_channel, get_mangas_on_channel, get_manga, \
    add_to_channel, update_manga, get_all_channels_id, remove_from_channel

guilds_ids: list | None = []

if t := os.getenv("TESTING_GUILD_ID"):
    guilds_ids.append(t)
else:
    guilds_ids = None


def get_unregister_autocomplete(ctx: discord.AutocompleteContext) -> list[str]:
    target = ctx.options["channel"] if ctx.options["channel"] else ctx.interaction.channel_id
    if not is_channel_registered(target):
        return []
    return [manga.title for manga in get_mangas_on_channel(channel_id=target)]


class CorrectMangaView(discord.ui.View):
    def __init__(self, author, chapter: S_MangaChapter, title: str):
        super().__init__()
        self._author = author
        self._chapter = chapter
        self._title = title

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self._author.id

    def disable_buttons(self):
        self.stop()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary, emoji="✅")
    async def yes(self, _, interaction: discord.Interaction):
        try:
            database.add_manga_to_channel(title=self._title, manga=self._chapter, channel_id=interaction.channel_id)
        except Exception as e:
            return await interaction.response.send_message(f"Error: {e}", ephemeral=True)
        else:
            await interaction.message.add_reaction("✅")
            await interaction.response.edit_message(view=self)
        finally:
            self.disable_buttons()

    @discord.ui.button(label="No", style=discord.ButtonStyle.primary, emoji="❌")
    async def no(self, _, interaction: discord.Interaction):
        self.disable_buttons()
        await interaction.message.add_reaction("❌")
        return await interaction.response.edit_message(view=self)


class Manga(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.notify_new_releases.start()

    @tasks.loop(minutes=5)
    async def notify_new_releases(self):
        log.debug("Searching for releases...")

        for channel_id in get_all_channels_id():
            channel = self.bot.get_channel(channel_id)
            if not channel:
                log.warning(f"channel {channel_id} not found")
                continue
            releases = []
            for manga in get_mangas_on_channel(channel_id=channel_id):
                chapter = await _get_new_chapter_info(manga.title)
                if chapter:
                    releases.append(format_response(chapter))
                    update_manga(manga.title, chapter.number)
            for release in releases:
                await channel.send(release)

        log.info("Finished searching for releases")

    @discord.slash_command(description="Find the latest chapter for a given manga", guild_ids=guilds_ids)
    @discord.option("title", type=str, description="The title of the manga to search for", required=True)
    @discord.option("chapter", type=int, description="The chapter to search for", required=False)
    async def search(self, ctx, title: str, chapter: int | None = None):
        if chapter < 0:
            return await ctx.respond(f"Chapter must be a positive number !")

        query = f"{title} {chapter}" if chapter else title

        if m := await reddit.notsync.search_manga(query):
            embed = discord.Embed(color=discord.Color.blurple())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.title = "Found something !"
            embed.add_field(name="Title", value=m.title)
            embed.add_field(name="Chapter", value=str(m.number))
            embed.add_field(name="Chapter link", value=m.link, inline=False)
            return await ctx.respond(embed=embed)
        else:
            return await ctx.respond(f"Did not found the manga !")

    @discord.slash_command(description="Setup the bot for this channel", guild_ids=guilds_ids)
    @discord.option("channel", type=discord.TextChannel, description="The channel to setup the bot for", )
    async def setup(self, ctx: discord.ApplicationContext, channel: discord.TextChannel | None = None):
        channel = channel if channel else ctx.channel
        channel_info = get_channel(channel.id)

        if channel_info is None:
            create_channel(channel.id)
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

        if not is_channel_registered(channel.id):
            embed = discord.Embed(title=f"{channel.mention}'s tracked manga", description="Nothing registered",
                                  color=discord.Color.blurple())
            return await ctx.respond(embed=embed)

        if mangas := get_mangas_on_channel(channel.id):
            response = [f"{manga.title}: **{manga.last_chapter}**" for manga in mangas]
            embed = discord.Embed(title=f"{channel.mention}'s tracked manga", description="\n".join(response),
                                  color=discord.Color.blurple())
            return await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=f"{channel.mention}'s tracked manga", description="Nothing registered",
                                  color=discord.Color.blurple())
            return await ctx.respond(embed=embed)

    @discord.slash_command(
        description="Register a manga to receive notifications when a new chapter is released",
        guild_ids=guilds_ids
    )
    @discord.option("channel", type=discord.TextChannel, description="The channel to register the manga on",
                    required=True)
    @discord.option("title", type=str, description="The title of the manga to search for", required=True)
    async def register(self, ctx: discord.commands.context.ApplicationContext, channel: discord.TextChannel,
                       title: str):
        channel: discord.TextChannel = channel if channel else ctx.channel

        await ctx.defer()

        if not is_channel_registered(channel.id):
            return await ctx.followup.send(f"Please use /setup on {channel.mention} first", ephemeral=True)

        if ms := get_mangas_on_channel(channel_id=channel.id):
            for m in ms:
                if m.title.lower() == title.lower():
                    return await ctx.followup.send(f"**{title}** is already registered")

        if get_manga(title=title):
            if add_to_channel(channel_id=channel.id, title=title):
                return await ctx.followup.send(f"Registered **{title}** on {channel.mention}")
            else:
                return await ctx.followup.send(f"Error", ephemeral=True)

        if m := await reddit.notsync.search_manga(title):
            return await ctx.followup.send(
                f"{m.title}\n{m.link}, is this correct ?",
                view=CorrectMangaView(author=ctx.author, chapter=m, title=title)
            )

        return await ctx.followup.send(f"Did not found **{title}**")

    @discord.slash_command(
        description="Unregister a manga to stop receiving notifications when a new chapter is released",
        guild_ids=guilds_ids,
    )
    @discord.option(name="title", type=str, required=True, autocomplete=get_unregister_autocomplete,
                    description="The REGISTERED title of the manga to remove", )
    @discord.option(name="channel", type=discord.TextChannel, description="The channel to unregister the manga from",
                    required=True)
    async def unregister(self, ctx: discord.commands.context.ApplicationContext, channel: discord.TextChannel,
                         title: str):
        await ctx.defer()

        channel: discord.TextChannel = channel if channel else ctx.channel

        if channel.guild != ctx.guild:
            return await ctx.followup.send("This channel is not from this server", ephemeral=True)

        if not is_channel_registered(channel.id):
            return await ctx.followup.send(f"Please use /setup on {channel.mention} first", ephemeral=True)

        if not (get_manga(title=title)):
            return await ctx.followup.send(f"**{title}** is unregistered on {channel.mention}")

        if remove_from_channel(channel_id=channel.id, title=title):
            return await ctx.followup.send(f"Removed **{title}** from {channel.mention}")

        return await ctx.followup.send("Error", ephemeral=True)


async def _get_new_chapter_info(title: str) -> S_MangaChapter | None:
    if not (m := get_manga(title=title)):
        log.error(f"Error while searching for {title}: Manga not registered")
        log.debug(f"Did not found: {title}")
        return None

    try:
        result = await reddit.notsync.search_manga(title)
    except Exception as e:
        log.error(f"Error while searching for {title}: {e}")
        log.debug(f"Did not found: {title}")
        return None

    if not result:
        log.debug(f"Did not found: {title}")
        return None

    if result.number <= m.last_chapter:
        log.debug(f"No new chapters for: {title} (last chapter: {m.last_chapter})")
        return None

    if not result.link:
        log.debug("Found new chapter but no link were provided")
        return S_MangaChapter(title=title, number=result.number, link=None)

    log.debug(f"Found new chapter for: {title} (last chapter: {m.last_chapter})")
    return S_MangaChapter(title=title, number=result.number, link=result.link)


def setup(bot):
    bot.add_cog(Manga(bot))
