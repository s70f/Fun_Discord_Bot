import discord as discord
from discord.ext import commands
import random
import time


class War(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data = {}

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("please dont spam")

    @commands.command()
    async def army(self, ctx):
        army = discord.Embed(
            colour=discord.Colour.blue()
        )

        army.set_footer(
            text="Use '.attack' to attack your enemy or '.enemy' to see their army")
        army.set_thumbnail(url=ctx.author.avatar_url)
        army.add_field(
            name=f"Army Name", value=f"🔺 {ctx.author.display_name}'s Army", inline=False)
        army.add_field(
            name='Soldiers', value=f"🍢 {self.data[ctx.author.id]['soldiers_1']}", inline=False)
        army.add_field(
            name='Catapult Ammo', value=f"💣 {self.data[ctx.author.id]['ammo_1']}", inline=False)
        army.add_field(
            name='Cavalry', value='Disabled', inline=False)
        army.add_field(
            name='Pikeman', value='Disabled', inline=False)
        army.add_field(
            name='Shields', value='Disabled', inline=False)
        army.add_field(
            name='Damage Dealt', value=f"🔸 {self.data[ctx.author.id]['dealt']}", inline=False)
        army.add_field(
            name='Damage Taken', value=f"🔹 {self.data[ctx.author.id]['taken']}", inline=False)

        await ctx.send(embed=army)

    @commands.command()
    async def enemy(self, ctx):
        enemy = discord.Embed(
            title="Bot's Army",
            colour=discord.Colour.red()
        )

        enemy.add_field(
            name='Soldiers', value=f"🍢 {self.data[self.game_id]['soldiers_2']}", inline=False)
        enemy.add_field(
            name='Catapult Ammo', value=f"💣 {self.data[self.game_id]['ammo_2']}", inline=False)

        await ctx.send(embed=enemy)

    @commands.command()
    async def war(self, ctx):
        if ctx.author.id in self.data.keys():
            await ctx.send('You have already started a battle')
        else:

            print(self.data)
            self.game_id = 768984833279262760 + ctx.author.id

            soldiers_1 = random.randint(25, 40)
            soldiers_2 = random.randint(25, 40)

            dealt = 0
            taken = 0

            self.data[ctx.author.id] = {
                'soldiers_1': soldiers_1, 'dealt': dealt, 'taken': taken, 'ammo_1': random.randint(1, 3)}
            self.data[self.game_id] = {
                'soldiers_2': soldiers_2, 'ammo_2': random.randint(1, 3)}
            print(self.data)

            await self.army(ctx)
            await ctx.send("-" * 16)

    async def bot_attack(self, ctx):
        damage = random.randint(3, 9)
        self.data[self.game_id]['soldiers_2'] -= damage
        self.data[ctx.author.id]['taken'] += damage
        dmg = discord.Embed(
            title="Take Cover!",
            description=f"""`{damage}` of your soldiers were killed in battle
                            `{self.data[ctx.author.id]['soldiers_1']}` of your soldiers remain""",
            colour=discord.Colour.red()
        )

        await ctx.send(embed=dmg)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def attack(self, ctx):
        if ctx.author.id in self.data.keys():
            damage = random.randint(3, 9)
            self.data[self.game_id]['soldiers_2'] -= damage
            self.data[ctx.author.id]['dealt'] += damage
            print(self.data)
            dmg = discord.Embed(
                title="Attack!",
                description=f"""**You killed** `{damage}` enemy soldiers
                                You have killed a **total** of `{self.data[ctx.author.id]['dealt']}` enemy soldiers""",
                colour=discord.Colour.orange()
            )

            await ctx.send(embed=dmg)
            await ctx.send("-" * 16)
            time.sleep(2)

            await self.bot_attack(ctx)

        else:
            await ctx.send("please use the `.war` command to start a battle")


def setup(client):
    client.add_cog(War(client))
