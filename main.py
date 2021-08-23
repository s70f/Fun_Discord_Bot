# import
import discord
from discord.ext import commands
import os

# intents
intents = discord.Intents.all()
intents.members = True

# command prefix
client = commands.Bot(command_prefix='.')

# load/unload files


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(filename)
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print("Bot is ready")

f = open("token.txt", "r")
BOT_TOKEN = f.read()  # I am 100 iq

client.run(BOT_TOKEN)
