import discord


class BaseEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_author(name="Robbot", icon_url="https://i.imgur.com/4M34hi2.png")


class ErrorEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title="Error",
            description=description,
            color=discord.Colour.red()
        )


class MangaInfoEmbed(BaseEmbed):
    def __init__(self,
                 title: str,
                 description: str | None = None,
                 image_url: str | None = None,
                 year: str | None = None,
                 alternative_titles: list[str] | None = None,
                 chapters: int | None = None,
                 status: str | None = None,
                 authors: list[str] | None = None,
                 artists: list[str] | None = None,
                 ):
        super().__init__(
            title=title,
            description=description,
            color=discord.Colour.blurple(),

        )
        if image_url:
            self.set_image(url=image_url)
        if alternative_titles:
            self.add_field(name="Alternative Titles", value="\n".join(alternative_titles), inline=False)
        if year:
            self.add_field(name="Year", value=year, inline=True)
        if chapters:
            self.add_field(name="Chapters", value=str(chapters), inline=True)
        if status:
            self.add_field(name="Status", value=status, inline=True)

        if authors == artists:
            self.add_field(name="Authors & Artists", value="\n".join(authors), inline=True)
        else:
            if authors:
                self.add_field(name="Authors", value="\n".join(authors), inline=True)
            if artists:
                self.add_field(name="Artists", value="\n".join(artists), inline=True)
