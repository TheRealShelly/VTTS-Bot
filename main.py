import discord
from discord import app_commands
from discord.ext import commands
from db import DB, UserRepository

import asyncio

import os
import time

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

database = DB(URI, DB_NAME)

async def main():
    database.connect()

    try:
        await bot.start(TOKEN)
    finally:
        await bot.close()
        await database.close()
        print('database connection ended')

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
        await interaction.followup.send(f"couldnt sync commands, err: {e}", ephemeral=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exiting')
