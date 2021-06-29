import discord as discord
from discord.ext import commands
import json

class classes(commands.Cog):

    def __init__(self, client):
        self.client = client

    # TODO:Make diff classes show diff embeds
    async def sniper_class(self, ctx):
        '''shows current class'''
        with open('user_data.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)

        current_main = discord.Embed(
            description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
            colour=discord.Colour.green()
        )
        current_main.set_author(name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
        current_main.add_field(name="• Increase Minimum Damage", value="Strength: `1/2`\nCost: `$0`", inline=False)
        current_main.add_field(name="• Decrease Maximum Soldiers", value="Weakness: `1/2`\nCost: `Follows Strength`", inline=False)
        current_main.add_field(name="• Class Stats", value="Minimum Damage `-1`\nMaximum Soldier `-5`", inline=False)
        await ctx.send(embed=current_main)

    async def marksmen_class(self, ctx):
        '''shows current class'''
        with open('user_data.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)

        current_main = discord.Embed(
            description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
            colour=discord.Colour.green()
        )
        current_main.set_author(name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
        current_main.add_field(name="• Increase Minimum Soldiers", value="Strength: `1/3`\nCost: `$0`", inline=False)
        current_main.add_field(name="• Decrease Maximum Damage", value="Weakness: `1/3`\nCost: `Follows Strength`", inline=False)
        current_main.add_field(name="• Class Stats", value="Minimum Soldiers: `+5`\nMaximum Damage: `-1`", inline=False)
        await ctx.send(embed=current_main)

    async def infantry_class(self, ctx):
        '''shows current class'''
        with open('user_data.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)

        current_main = discord.Embed(
            description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
            colour=discord.Colour.green()
        )
        current_main.set_author(name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
        current_main.add_field(name="• Soldier Count", value="Strength: `1/3`\nCost: `$0`", inline=False)
        current_main.add_field(name="• Decrease Maximum Damage", value="Weakness: `1/3`\nCost: `Follows Strength`", inline=False)
        current_main.add_field(name="• Class Stats", value="Soldier Count: `+5`\nNot Able to Activate Rage or Cavalry", inline=False)
        await ctx.send(embed=current_main)
        
    async def artillery_class(self, ctx):
        '''shows current class'''
        with open('user_data.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)

        current_main = discord.Embed(
            description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
            colour=discord.Colour.green()
        )
        current_main.set_author(name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
        current_main.add_field(name="• Ammo Count", value="Strength: `1/2`\nCost: `$0`", inline=False)
        current_main.add_field(name="• Soldier Count", value="Weakness: `1/2`\nCost: `Follows Strength`", inline=False)
        current_main.add_field(name="• Class Stats", value="Ammo Count: `+1`\nSoldier Count: `-6` (upgraded strengt is -12)", inline=False)
        await ctx.send(embed=current_main)
    
    @commands.group(invoke_without_command=True)
    async def main(self, ctx):
        with open('user_data.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)
        
        if data[str(ctx.author.id)]['class'] == "sniper":
            await self.sniper_class(ctx)
        
        if data[str(ctx.author.id)]['class'] == "marksmen":
            await self.marksmen_class(ctx)
        
        if data[str(ctx.author.id)]['class'] == "infantry":
            await self.infantry_class(ctx)

        if data[str(ctx.author.id)]['class'] == "artillery":
            await self.artillery_class(ctx)
        
    @main.command()
    async def change(self, ctx, arg : str):
        self.available_classes = ["sniper", "marksmen", "artillery", "infantry"]
        with open('user_data.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)   
            data[str(ctx.author.id)]['class'] = arg

            if arg in data[str(ctx.author.id)]['unlocked']:
                with open('user_data.json', 'w') as user_id:
                    json.dump(data, user_id, indent=2)

                current_main = discord.Embed(
                    title="Class",
                    description=f"You changed your class to **{data[str(ctx.author.id)]['class']}**",
                    colour=discord.Colour.green()
                )
                
                current_main.set_author(name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=current_main)

            elif arg in self.available_classes:
                await ctx.send(f"You dont have {arg} unlocked yet")
            else:
                await ctx.send(f"{arg} is not a valid class name")
        
def setup(client):
    client.add_cog(classes(client))