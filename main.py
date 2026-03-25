import discord
from discord import app_commands
from discord.ext import commands

import asyncio

import os
import time
import random

from db import Client
from repositories import UserRepository, TTSRepository

import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
URI = os.getenv("CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")
 
admins = []
intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!", 
    intents=intents, 
    owner_id=798687278263304254
) 

client = Client(URI, DB_NAME)
db = client.connect()

users = UserRepository(db)
ttsmessages = TTSRepository(db)

def verify(func):
    async def inner(interaction: discord.Interaction):
        await users.getUser(interaction.user.id)
        return await func(interaction)
    return inner

async def main():
    try:
        await bot.start(TOKEN)
    finally:
        await bot.close()
        await client.close()
        print('client connection ended')

@bot.event
async def on_ready():
    channel = bot.get_channel(1085168423518093413) 
    ttime = time.time()
    message = await channel.send(
        f"**Gateway Ping:** `Calculating...`\
        \n**API Ping:** `Calculating...`"
    )
    await message.edit(content=
        f"**Gateway Ping:** `{round(bot.latency*1000)}ms`\
        \n**API Ping:** `{round((time.time() - ttime) * 1000)}ms`"
    )

    print(f"Logged as {bot.user}")


@bot.tree.command(name="sync",description="re-syncs all application commands on all servers")
async def sync(interaction: discord.Interaction):

    if interaction.user.id not in admins and interaction.user.id != bot.owner_id:
        await interaction.response.send_message(f"não pode usar isso fi...")
        return 0

    await interaction.response.defer(ephemeral=True)
    
    try:
        synced = await bot.tree.sync()
        await interaction.followup.send(f"synced {len(synced)} application command(s)", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"{e.__class__.__name__}: {e}", ephemeral=True)

@bot.tree.command(name="daily",description="me paga meu dinheiro")
@verify
async def daily(interaction: discord.Interaction):

    await interaction.response.defer()
    user = await users.getUser(interaction.user.id)

    left = time.time() - user['daily']
    if left < 86400:
        await interaction.followup.send(f"to liso veikkkk posso te pagar daqui a `{time.strftime("%Hh%Mm", time.gmtime(86400 - left))}`")
        return 0
    
    pix = random.randrange(15, 50)

    await users.updateUser(user['id'], {"atm": user['atm']+pix, "daily": time.time()})
    await interaction.followup.send(f"mandei o pix ai, agr tu ta com {user['atm']+pix} reais")

@bot.tree.command(name="atm", description="mostra quanto vc tem no pix")
@verify
async def atm(interaction: discord.Interaction):
    await interaction.response.defer()

    user = await users.getUser(interaction.user.id)
    await interaction.followup.send(f"você tem {user['atm']} {"real" if user['atm'] == 1 else 'reais'}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exiting')
