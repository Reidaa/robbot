import discord.ui
from bot.selects.MangaSearchSelectUI import MangaSearchSelectUI


class SearchMangaView(discord.ui.View):
    def __init__(self, options: list):
        super().__init__(timeout=30.0)
        self.select = MangaSearchSelectUI(options)
        self.add_item(self.select)


