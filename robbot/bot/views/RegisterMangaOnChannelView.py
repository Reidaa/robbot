from robbot.services.pocketbase.utils import AsyncPocketBaseUtils

import discord


class RegisterMangaOnChannelView(discord.ui.View):
    def __init__(self, author, title: str, pb_utils: AsyncPocketBaseUtils):
        super().__init__()
        self._author = author
        self._title = title
        self._pb_utils: AsyncPocketBaseUtils = pb_utils

    async def _callback(self, title: str, channel_id: int) -> bool:
        if not await self._pb_utils.is_manga_in_db(title):
            await self._pb_utils.register_manga(title)
        return await self._pb_utils.add_manga_to_channel(title, channel_id)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self._author.id

    def disable_buttons(self):
        self.stop()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary, emoji="✅")
    async def yes(self, _, interaction: discord.Interaction):
        try:
            await self._callback(self._title, interaction.channel_id)
        except Exception as e:
            return await interaction.response.send_message(f"Error: {e}", ephemeral=True)
        else:
            await interaction.message.add_reaction("✅")
            await interaction.response.edit_message(content="f", view=self)
        finally:
            self.disable_buttons()

    @discord.ui.button(label="No", style=discord.ButtonStyle.primary, emoji="❌")
    async def no(self, _, interaction: discord.Interaction):
        self.disable_buttons()
        await interaction.message.add_reaction("❌")
        return await interaction.response.edit_message(view=self)
