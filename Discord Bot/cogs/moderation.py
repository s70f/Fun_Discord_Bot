import discord as discord
from discord.ext import commands
import asyncio


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Clear
    @commands.command()
    async def clear(self, ctx, arg: int):
        amount = arg
        await ctx.channel.purge(limit=amount)

    # temp mute
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, mute_time: int):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f"{member.mention} was muted for {mute_time} seconds")

        await asyncio.sleep(mute_time)
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unmuted")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')


def setup(client):
    client.add_cog(Moderation(client))
