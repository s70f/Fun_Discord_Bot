import discord as discord
from discord.ext import commands
import random
import asyncio


class misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pfp(self, ctx, *, user: discord.Member = None):
        if not user:
            user = ctx.message.author
        embed = discord.Embed(
            title="Profile Picture",
            description=f"{user.mention}'s profile picture' ",
            color=0xecce8b
        )
        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def rainbow(self, ctx):

        cols = [0x32a852, 0x3296a8, 0xb700ff, 0x9232a8,
                0xa8326f, 0xf25207, 0x3efa00, 0xfa0000]
        embed = discord.Embed(
            title="RAINBOW",
            color=random.choice(cols)
        )

        msg = await ctx.send(embed=embed)

        for i in range(1000):
            embed2 = discord.Embed(
                title="RAINBOW",
                color=random.choice(cols)
            )
            await asyncio.sleep(0.1)
            await msg.edit(embed=embed2)


def setup(client):
    client.add_cog(misc(client))
