import { SlashCommandBuilder } from "discord.js";
import type { SlashCommand } from "../type";

export const ping: SlashCommand = {
  command: new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Replies with Pong!"),
  execute: async (interaction) => {
    await interaction.reply("Pong!");
  },
};
