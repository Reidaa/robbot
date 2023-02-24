from dotenv import load_dotenv
import discord
import os
from helper import cooldown
import re
import datetime

load_dotenv()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
            return

        if message.content[-4:].lower() == "quoi":
            return await on_quoi(message)

        if message.content.lower() == "feur":
            return await on_feur(message)

        if re.match(r'^([A-Za-z]+):\s*', message.content):
            return await on_citation(message)

@cooldown(60 * 5)
async def on_quoi(message):
    await message.reply(content="feur")
    return


@cooldown(60 * 5)
async def on_feur(message):
    await message.reply(content="https://media.discordapp.net/attachments/654847882477699105/981256511563112479/IMG_20220407_142209.jpg")
    return


async def on_citation(message):
    author = message.content[:message.content.find(":")]
    citation = message.content[message.content.find(":")+1:]
    print(author, datetime.datetime.now(), citation)
    return await message.reply("Je note")

async def on_weeb_mode(message):
    pass

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.presences = True
intents.members = True
client = MyClient(intents=intents)
client.run(os.getenv("TOKEN"))
