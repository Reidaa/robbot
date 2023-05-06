import os

import discord
from discord.ext import commands, tasks

import log
from robbot.db.database import PonyDB
from robbot.services import database
from robbot.services import reddit
from robbot.t import MangaChapter
from robbot.utils import format_response

db = PonyDB()

guilds_ids = []

if t := os.getenv("TESTING_GUILD_ID"):
    guilds_ids.append(t)


def get_unregister_autocomplete(ctx: discord.AutocompleteContext) -> list[str]:
    target = ctx.options["channel"] if ctx.options["channel"] else ctx.interaction.channel_id
    if not db.channel.unique(channel_id=target):
        return []
    return [manga.title for manga in db.manga.many(channel_id=target)]


class CorrectMangaView(discord.ui.View):
    def __init__(self, author, chapter: MangaChapter, title: str):
        super().__init__()
        self._author = author
        self._chapter = chapter
        self._title = title

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self._author.id

    def disable_buttons(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary, emoji="✅")
    async def yes(self, _, interaction: discord.Interaction):
        self.disable_buttons()
        try:
            database.add_manga_to_channel(title=self._title, manga=self._chapter, channel_id=interaction.channel_id)
        except Exception as e:
            return await interaction.response.send_message(f"Error: {e}", ephemeral=True)
        else:
            await interaction.message.add_reaction("✅")
            return await interaction.response.edit_message(view=self)

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

        for channel_id in db.channel.all():
            channel = self.bot.get_channel(channel_id)
            if not channel:
                log.warning(f"channel {channel_id} not found")
                continue
            releases = []
            for manga in db.manga.many(channel_id=channel_id):
                chapter = await _get_new_chapter_info(manga.title)
                if chapter:
                    releases.append(format_response(chapter))
                    db.manga.update(manga.title, chapter.number)
            for release in releases:
                await channel.send(release)

        log.info("Finished searching for releases")

    @discord.slash_command(description="Find the latest chapter for a given manga", guild_ids=guilds_ids)
    @discord.option("title", type=str, description="The title of the manga to search for", required=True)
    async def search(self, ctx, title: str):
        if m := await reddit.notsync.search_manga(title):
            return await ctx.respond(f"Found {m.title} {m.number} {m.link}")
        else:
            return await ctx.respond(f"Did not found the manga {ctx.author.mention}")

    @discord.slash_command(
        description="Display the list of mangas registered on this channel",
        guild_ids=guilds_ids
    )
    async def queue(self, ctx: discord.ApplicationContext, channel: discord.TextChannel | None = None):
        target: int = channel.id if channel else ctx.channel_id

        if not db.channel.unique(channel_id=target):
            return await ctx.respond("Nothing registered")

        if mangas := db.manga.many(channel_id=target):
            response = [f"{manga.title} - {manga.last_chapter}" for manga in mangas]
            return await ctx.respond("\n".join(response))
        else:
            return await ctx.respond("Nothing registered here")

    @discord.slash_command(
        description="Register a manga to receive notifications when a new chapter is released",
        guild_ids=guilds_ids
    )
    @discord.option("title", type=str, description="The title of the manga to search for", required=True)
    @discord.option("channel", type=discord.TextChannel, description="The channel to register the manga to")
    async def register(self, ctx: discord.commands.context.ApplicationContext, title: str,
                       channel: discord.TextChannel | None = None):
        await ctx.defer()

        target: int = channel.id if channel else ctx.channel_id

        if not db.channel.unique(channel_id=target):
            db.channel.create(channel_id=target)

        if ms := db.manga.many(channel_id=target):
            for m in ms:
                if m.title.lower() == title.lower():
                    return await ctx.followup.send(f"**{title}** is already registered")

        if db.manga.unique(title=title):
            if db.channel.update(channel_id=target, title=title):
                return await ctx.followup.send(f"Registered **{title}** on {channel.mention}")
            else:
                return await ctx.followup.send(f"Error")

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
    @discord.option(
        name="title", type=str, required=True, autocomplete=get_unregister_autocomplete,
        description="The REGISTERED title of the manga to remove",
    )
    @discord.option(name="channel", type=discord.TextChannel, description="The channel to unregister the manga from",
                    required=True)
    async def unregister(self, ctx: discord.commands.context.ApplicationContext, channel: discord.TextChannel,
                         title: str):
        await ctx.defer()

        channel: discord.TextChannel = channel if channel else ctx.channel

        if channel.guild != ctx.guild:
            return await ctx.followup.send("This channel is not from this server", ephemeral=True)

        if not (db.channel.unique(channel_id=channel.id)):
            return await ctx.followup.send(f"Nothing to remove on channel {channel.mention}")

        if not (db.manga.unique(title=title)):
            return await ctx.followup.send(f"**{title}** has not been registered at all")

        if db.channel.remove(channel_id=channel.id, title=title):
            return await ctx.followup.send(f"Removed **{title}** from {channel.mention}")

        return await ctx.followup.send("Error", ephemeral=True)


async def _get_new_chapter_info(title: str) -> MangaChapter | None:
    if not (manga := db.manga.unique(title=title)):
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

    if result.number <= manga.last_chapter:
        log.debug(f"No new chapters for: {title} (last chapter: {manga.last_chapter})")
        return None

    if not result.link:
        log.debug("Found new chapter but no link were provided")
        return MangaChapter(title=title, number=result.number, link=None)

    log.debug(f"Found new chapter for: {title} (last chapter: {manga.last_chapter})")
    return MangaChapter(title=title, number=result.number, link=result.link)


def setup(bot):
    bot.add_cog(Manga(bot))
