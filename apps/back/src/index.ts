import * as Sentry from "@sentry/bun";
import { hello } from "@robbot/core/index";
import { env } from "./env";
import {
  Client,
  Collection,
  Events,
  GatewayIntentBits,
  MessageFlags,
  REST,
} from "discord.js";
import type { SlashCommand } from "./type";
import { ping } from "./commands/ping";

Sentry.init({
  dsn: env.SENTRY_DSN,
});

function main() {
  // create a new Client instance
  const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent],
  });

  // listen for the client to be ready
  client.once(Events.ClientReady, (c) => {
    console.log(`Ready! Logged in as ${c.user.tag}`);
  });

  const slashCommands = new Collection<string, SlashCommand>();
  slashCommands.set(ping.command.name, ping);

  // const rest = new REST({ })

  client.on(Events.InteractionCreate, async (interaction) => {
    if (!interaction.isChatInputCommand()) return;
    const command = slashCommands.get(interaction.commandName);

    if (!command) {
      console.error(
        `No command matching ${interaction.commandName} was found.`,
      );
      return;
    }

    try {
      await command.execute(interaction);
    } catch (error) {
      console.error(error);
      if (interaction.replied || interaction.deferred) {
        await interaction.followUp({
          content: "There was an error while executing this command!",
          ephemeral: true,
        });
      } else {
        await interaction.reply({
          content: "There was an error while executing this command!",
          ephemeral: true,
        });
      }
    }
  });

  // login with the token from .env.local
  client
    .login(env.DISCORD_TOKEN)
    .catch((error) => console.error("Discord.Client.Login.Error", error));
}

main();
