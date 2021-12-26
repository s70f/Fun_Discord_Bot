import discord as discord
from discord import embeds
from discord.ext import commands
import json


class classes(commands.Cog):

    def __init__(self, client):
        self.client = client

    # TODO:Make diff classes show diff embeds
    with open('classes.json', 'r', encoding="utf8") as user_id:
        data = json.load(user_id)

        async def sniper_class(self, ctx, data):
            '''shows sniper class'''

            sniper = data[str(ctx.author.id)]['unlocked']['sniper']

            current_main = discord.Embed(
                description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
                colour=discord.Colour.green()
            )
            current_main.set_author(
                name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
            current_main.add_field(
                name="• Class Upgrades", value=f"Credits `+{sniper['cred_ups']}`\nStarting Soldiers `+{sniper['range_ups']}`", inline=False)
            current_main.add_field(
                name="• Class Stats", value=f"Starting Credits `{sniper['credits']}`\nStarting Soldiers `{sniper['range']}`", inline=False)
            await ctx.send(embed=current_main)

        async def marksmen_class(self, ctx, data):
            '''shows marksmen class'''

            marksmen = data[str(ctx.author.id)]['unlocked']['marksmen']

            current_main = discord.Embed(
                description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
                colour=discord.Colour.green()
            )
            current_main.set_author(
                name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
            current_main.add_field(
                name="• Class Upgrades", value=f"Credits `+{marksmen['cred_ups']}`\nStarting Soldiers `+{marksmen['range_ups']}`", inline=False)
            current_main.add_field(
                name="• Class Stats", value=f"Starting Credits `{marksmen['credits']}`\nStarting Soldiers `{marksmen['range']}`", inline=False)
            await ctx.send(embed=current_main)

        async def infantry_class(self, ctx, data):
            '''shows infantry class'''

            infantry = data[str(ctx.author.id)]['unlocked']['infantry']

            current_main = discord.Embed(
                description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
                colour=discord.Colour.green()
            )
            current_main.set_author(
                name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
            current_main.add_field(
                name="• Class Upgrades", value=f"Credits `+{infantry['cred_ups']}`\nStarting Soldiers `+{infantry['range_ups']}`", inline=False)
            current_main.add_field(
                name="• Class Stats", value=f"Starting Credits `{infantry['credits']}`\nStarting Soldiers `{infantry['range']}`", inline=False)
            await ctx.send(embed=current_main)

        async def artillery_class(self, ctx, data):
            '''shows artillery class'''

            artillery = data[str(ctx.author.id)]['unlocked']['artillery']

            current_main = discord.Embed(
                description=f"**{data[str(ctx.author.id)]['class']}**\n*use `.main change` to change your class!*",
                colour=discord.Colour.green()
            )
            current_main.set_author(
                name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
            current_main.add_field(
                name="• Class Upgrades", value=f"Credits `+{artillery['cred_ups']}`\nStarting Soldiers `+{artillery['range_ups']}`", inline=False)
            current_main.add_field(
                name="• Class Stats", value=f"Starting Credits `{artillery['credits']}`\nStarting Soldiers `{artillery['range']}`", inline=False)
            await ctx.send(embed=current_main)

    @commands.group(invoke_without_command=True)
    async def main(self, ctx):
        with open('classes.json', 'r', encoding="utf8") as classes:
            data = json.load(classes)

        if data[str(ctx.author.id)]['class'] == "sniper":
            await self.sniper_class(ctx, data)

        if data[str(ctx.author.id)]['class'] == "marksmen":
            await self.marksmen_class(ctx, data)

        if data[str(ctx.author.id)]['class'] == "infantry":
            await self.infantry_class(ctx, data)

        if data[str(ctx.author.id)]['class'] == "artillery":
            await self.artillery_class(ctx, data)

    @main.command()
    async def change(self, ctx, arg: str):
        self.available_classes = [
            "sniper", "marksmen", "artillery", "infantry"]
        with open('classes.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)
            data[str(ctx.author.id)]['class'] = arg

            if arg in data[str(ctx.author.id)]['unlocked']:
                with open('classes.json', 'w') as user_id:
                    json.dump(data, user_id, indent=2)

                current_main = discord.Embed(
                    title="Class",
                    description=f"You changed your class to **{data[str(ctx.author.id)]['class']}**",
                    colour=discord.Colour.green()
                )

                current_main.set_author(
                    name="Current Class | " + ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=current_main)

            elif arg in self.available_classes:
                await ctx.send(f"You dont have {arg} unlocked yet")
            else:
                await ctx.send(f"{arg} is not a valid class name")

    @commands.command(aliases=['wins', 'losses', 'gold'])
    async def stats(self, ctx):
        with open('classes.json', 'r', encoding="utf8") as user_id:
            data = json.load(user_id)
            wins = data[str(ctx.author.id)]['stats']["wins"]
            lost = data[str(ctx.author.id)]['stats']["losses"]
            gold = data[str(ctx.author.id)]['stats']["gold"]

        current_wins = discord.Embed(
            description="",
            colour=discord.Colour.blurple()
        )
        current_wins.set_author(
            name="Current stats | " + ctx.author.name, icon_url=ctx.author.avatar_url)

        current_wins.add_field(name="Wins", value=f"🏆 {wins}", inline=False)
        current_wins.add_field(name="Losses", value=f"🥀 {lost}", inline=False)
        current_wins.add_field(name="Gold", value=f"💸 {gold}", inline=False)

        await ctx.send(embed=current_wins)


def setup(client):
    client.add_cog(classes(client))
