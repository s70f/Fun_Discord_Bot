import discord as discord
from discord.ext import commands

class misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pfp(self, ctx, *, user: discord.Member=None):
        if not user:
            user = ctx.message.author
        embed = discord.Embed(
            title="Profile Picture", 
            description=f"{user.mention}'s profile picture' ",
            color=0xecce8b
        )
        embed.set_image(url=user.avatar_url)    

        await ctx.send(embed=embed)
        
def setup(client):
    client.add_cog(misc(client))