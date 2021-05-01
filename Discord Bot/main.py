# import
import discord
from discord.ext import commands
from discord.ext import tasks
import os

# intents
intents = discord.Intents.all()
intents.members = True

# command prefix
client = commands.Bot(command_prefix='.')


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
        client.load_extension(f'cogs.{filename[:-3]}')


client.run('NzY4OTg0ODMzMjc5MjYyNzYw.X5Ia7w._YqoRjS8OG4hPbSZeWDwUJ4b0S0')
