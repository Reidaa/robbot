import type {
  SlashCommandBuilder,
  CommandInteraction,
  AutocompleteInteraction,
  Interaction,
} from "discord.js";

type CommandCallback = (interaction: CommandInteraction) => Promise<void>;
type AutocompleteCommandCallback = (
  interaction: AutocompleteInteraction,
) => Promise<void>;

export type SlashCommand = {
  command: SlashCommandBuilder;
  execute: CommandCallback;
  autocomplete?: AutocompleteCommandCallback;
  cooldownSeconds?: number;
};
