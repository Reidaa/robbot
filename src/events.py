import datetime

from discord import Message

from helper import cooldown


@cooldown(60 * 5)
async def on_quoi(message: Message):
    await message.reply(content="feur")
    return


@cooldown(60 * 5)
async def on_feur(message: Message):
    await message.reply(
        content="https://media.discordapp.net/attachments/654847882477699105/981256511563112479/IMG_20220407_142209.jpg")
    return


async def on_citation(message: Message):
    author = message.content[:message.content.find(":")]
    citation = message.content[message.content.find(":") + 1:]
    print(author, datetime.datetime.now(), citation)
    return await message.reply("Je note")
