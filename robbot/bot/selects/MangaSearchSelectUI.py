import asyncio

import discord
from discord import Interaction
from robbot.bot.Embeds import MangaInfoEmbed
from robbot.services.mangaupdate import utils as mangaupdate
from robbot.services.anilist import utils as anilist

from robbot.utils import cleanhtml


class MangaSearchSelectUI(discord.ui.Select):
    def __init__(self, options: list[dict[str, any]]):
        self.finished = False
        self._mangas_select = []
        self._options = options
        self._parse()
        super().__init__(
            options=self._mangas_select,
            min_values=1,
            max_values=1
        )

    def _parse(self):
        for idx, option in enumerate(self._options):
            label = f"{option['title']} ({option['year']})"
            if option["hit_title"]:
                description = f"{option['hit_title']}"
            else:
                description = None
            self._mangas_select.append(
                discord.SelectOption(
                    label=label,
                    description=description,
                    value=str(idx)
                )
            )

    async def callback(self, interaction: Interaction):
        selected = self._options[int(self.values[0])]
        mu_info, anilist_info = await asyncio.gather(
            mangaupdate.get_manga_info(selected["series_id"]),
            anilist.get_manga_info(selected["title"])
        )

        description = None
        if anilist_info["description"]:
            description = cleanhtml(anilist_info["description"])

        match anilist_info["status"]:
            case "FINISHED":
                status = "Finished"
            case "RELEASING":
                status = "Ongoing"
            case "NOT_YET_RELEASED":
                status = "Not yet released"
            case "CANCELLED":
                status = "Cancelled"
            case "HIATUS":
                status = "On Hiatus"
            case _:
                status = "Unknown"

        titles = []
        if anilist_info["title"]["english"]:
            titles.append(anilist_info["title"]["english"])
        if anilist_info["title"]["native"]:
            titles.append(anilist_info["title"]["native"])

        authors = []
        artists = []
        for author in mu_info.authors:
            if author["type"] == "Author":
                authors.append(author["name"])
            if author["type"] == "Artist":
                artists.append(author["name"])

        embed = MangaInfoEmbed(
            title=anilist_info["title"]["romaji"],
            description=description,
            image_url=anilist_info["coverImage"]["extraLarge"],
            year=anilist_info["startDate"]["year"],
            alternative_titles=titles,
            chapters=mu_info.latest_chapter,
            status=status,
            authors=authors,
            artists=artists

        )
        await interaction.response.edit_message(content=None, embed=embed, view=None)
        self.finished = True
