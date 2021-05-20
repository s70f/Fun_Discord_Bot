import discord as discord
from discord.ext import commands
import random
import time


class War(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data = {}

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send("please dont spam")

    @commands.command()
    async def army(self, ctx):
        if ctx.author.id not in self.data.keys():
            await ctx.send("You have not started a battle yet. Use '.war' to start one")
        else:
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
                name='Cavalry', value=self.data[ctx.author.id]['cavalry'], inline=False)
            army.add_field(
                name='Pikeman', value=self.data[ctx.author.id]['pikeman'], inline=False)
            army.add_field(
                name='Shields', value=self.data[ctx.author.id]['shields'], inline=False)
            army.add_field(
                name='Damage Dealt', value=f"🔸 {self.data[ctx.author.id]['dealt']}", inline=False)
            army.add_field(
                name='Damage Taken', value=f"🔹 {self.data[ctx.author.id]['taken']}", inline=False)

            await ctx.send(embed=army)

    @commands.command()
    async def enemy(self, ctx):
        if ctx.author.id not in self.data.keys():
            await ctx.send("You have not started a battle yet. Use '.war' to start one")
        else:
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

            self.data[ctx.author.id] = {
                'soldiers_1': soldiers_1, 'dealt': 0, 'taken': 0, 'ammo_1': random.randint(1, 3), 'cavalry': False, 'pikeman': False, 'shields': False}
            self.data[self.game_id] = {
                'soldiers_2': soldiers_2, 'ammo_2': random.randint(1, 3)}
            print(self.data)

            await self.army(ctx)
            await ctx.send("-" * 16)

    async def bot_attack(self, ctx):
        damage = random.randint(3, 9)
        self.data[ctx.author.id]['soldiers_1'] -= damage
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
            print(damage)
            if self.data[ctx.author.id]['cavalry'] == True:
                damage += 2
            elif self.data[ctx.author.id]['pikeman'] == True:
                damage -= 2
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

    @commands.group(invoke_without_command=True)
    async def enable(self, ctx):
        enable_help = discord.Embed(
                title="War | Enable",
                description="Use `.enable [type]` to enable different army types!",
                colour=discord.Colour.gold()
            )
        enable_help.add_field(
            name='Cavalry', value=f"Enables Cavalry: guaranteed +2 attack damage on every attack but sacrifices 10 soldiers", inline=False)
        enable_help.add_field(
            name='Pikeman', value=f"Enables Pikeman: +10 soldiers but -2 damage on every attack", inline=False)
        enable_help.add_field(
            name='Shields', value=f"Enables Shields: -1 damage taken on enemy attacks", inline=False)
        await ctx.send(embed=enable_help)

    @enable.command()
    async def cavalry(self, ctx):
        self.data[ctx.author.id]['cavalry'] = True
        self.data[ctx.author.id]['soldiers_1'] -= 10

        cavalry_enable = discord.Embed(
                title="War | Cavalry Enabled",
                description="Enables Cavalry: guaranteed +2 attack damage on every attack but sells 10 of your soldiers for horses",
                colour=discord.Colour.purple()
            )

        await ctx.send(embed=cavalry_enable)
    
    @enable.command()
    async def pikeman(self, ctx):
        self.data[ctx.author.id]['pikeman'] = True
        self.data[ctx.author.id]['soldiers_1'] += 10

        cavalry_enable = discord.Embed(
                title="War | Pikeman Enabled",
                description="Enables Pikeman: +10 soldiers but -2 damage on every attack",
                colour=discord.Colour.purple()
            )

        await ctx.send(embed=cavalry_enable)

def setup(client):
    client.add_cog(War(client))
