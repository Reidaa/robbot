import datetime
import os
import discord

from src.helpers import cooldown


@cooldown(60 * 5)
async def on_quoi(message: discord.Message):
    await message.reply(content="feur")
    return


@cooldown(60 * 5)
async def on_feur(message: discord.Message):
    await message.reply(content=os.getenv("FEUR"))
    return


async def on_citation(message: discord.Message):
    author = message.content[:message.content.find(":")]
    citation = message.content[message.content.find(":") + 1:]
    print(author, datetime.datetime.now(), citation)
    return await message.reply("Je note")


def is_leandre(user: discord.Member):
    username = f"{user.name}#{user.discriminator}"
    if username == os.getenv("LEANDRE"):
        return True
    else:
        return False

def is_quoi(message: str) -> bool:
    return message[-4:].lower() == "quoi"

def is_feur(message: str) -> bool:
    return message.lower() == "feur"

