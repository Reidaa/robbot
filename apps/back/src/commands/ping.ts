import { SlashCommandBuilder, Interaction } from "discord.js";

new SlashCommandBuilder()
  .setName("ping")
  .setDescription("Replies with Pong!")
  .toJSON();

async function execute(interaction) {
  await interaction.reply("Pong!");
}
