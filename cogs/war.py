import discord as discord
from discord.ext import commands
import random
import json
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Battle(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data = {}
        self.id = {}
        self.market = {}
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send("please dont spam")

    @commands.command(aliases=['m'])
    async def market(self, ctx):
        market = discord.Embed(
            title="Market",
            descrition="Here you will find all your attack prices",
            colour=discord.Colour.dark_green()
        )

        market.add_field(
            name="Light Attack", value=f"💸 {self.market[self.game_id]['light']}", inline=False)
        market.add_field(
            name="Heavy Attack", value=f"💸 {self.market[self.game_id]['heavy']}", inline=False)
        market.add_field(
            name="Catapults", value=f"💸 {self.market[self.game_id]['catapult']}", inline=False)
        market.add_field(
            name="Assassins", value=f"💸 {self.market[self.game_id]['assassin']}", inline=False)
        await ctx.send(embed=market)

    async def turn(self, ctx):
        self.id[self.id[ctx.author.id]['enemy']]['turn'] = True
        self.id[ctx.author.id]['turn'] = False

        self.market[self.game_id] = {
            "light": random.randint(3, 10), "heavy": random.randint(15, 30), "catapult": random.randint(30, 50), "assassin": random.randint(6, 14)}

        await self.market(ctx)

    async def death(self, ctx):
        if self.data[self.id[ctx.author.id]['enemy']]['soldiers'] <= 0:
            dead = discord.Embed(
                title="Dead!",
                description=f"It has been an honor fighting with you",
                colour=discord.Colour.dark_red()
            )
            await ctx.send(embed=dead)

    @cog_ext.cog_slash(name="Army", description="Shows your army in your current battle", guild_ids=[872981627570114561])
    async def view_army(self, ctx: SlashContext):
        await self.army(ctx)

    @commands.command()
    async def army(self, ctx: SlashContext):
        if ctx.author.id not in self.data.keys():
            await ctx.send("You have not started a battle yet. Use '.war' to start one")
        else:
            army = discord.Embed(
                colour=discord.Colour.teal()
            )

            army.set_footer(
                text="Use '.attack' to attack your enemy or '.enemy' to see their army")
            army.set_thumbnail(url=ctx.author.avatar_url)
            print(ctx.author)
            army.add_field(
                name="Army Name", value=f"🔺 {ctx.author.display_name}'s Army", inline=False)
            army.add_field(
                name='Soldiers', value=f"🍢 {self.data[ctx.author.id]['soldiers']}", inline=False)
            army.add_field(
                name='Catapult Ammo', value=f"💣 {self.data[ctx.author.id]['ammo']}", inline=False)
            army.add_field(
                name='Credits', value=f"💸 {self.data[ctx.author.id]['credits']}", inline=False)
            army.add_field(
                name='Damage Dealt', value=f"🔸 {self.data[ctx.author.id]['dealt']}", inline=False)
            army.add_field(
                name='Damage Taken', value=f"🔹 {self.data[ctx.author.id]['taken']}", inline=False)

            await ctx.send(embed=army)

    @commands.command()
    async def enemy(self, ctx):
        if ctx.author.id not in self.id.keys():
            await ctx.send("You have not started a battle yet. Use '.war' to start one")
        else:

            arg = self.id[ctx.author.id]['enemy_user']

            enemy = discord.Embed(
                # title="Bot's Army",
                colour=discord.Colour.dark_teal()
            )

            enemy.set_footer(
                text="Use '.attack' to attack your enemy or '.enemy' to see their enemy")
            enemy.set_thumbnail(url=arg.avatar_url)
            enemy.add_field(
                name=f"enemy Name", value=f"🔻 {arg.display_name}'s enemy", inline=False)
            enemy.add_field(
                name='Soldiers', value=f"🍢 {self.data[arg.id]['soldiers']}", inline=False)
            enemy.add_field(
                name='Catapult Ammo', value=f"💣 {self.data[arg.id]['ammo']}", inline=False)
            enemy.add_field(
                name='Damage Dealt', value=f"🔸 {self.data[arg.id]['dealt']}", inline=False)
            enemy.add_field(
                name='Damage Taken', value=f"🔹 {self.data[arg.id]['taken']}", inline=False)

            await ctx.send(embed=enemy)

    @commands.command(aliases=['w'])
    async def war(self, ctx, arg: discord.Member):
        if ctx.author.id in self.id.keys():
            await ctx.send('You have already started a battle')
        else:
            with open('classes.json', 'r', encoding="utf8") as user_id:
                self.class_data = json.load(user_id)

            num_range_0 = self.class_data[str(
                ctx.author.id)]['unlocked'][self.class_data[str(ctx.author.id)]["class"]]["range"]
            num_credits_0 = self.class_data[str(
                ctx.author.id)]['unlocked'][self.class_data[str(ctx.author.id)]["class"]]["credits"]
            num_range_1 = self.class_data[str(
                arg.id)]['unlocked'][self.class_data[str(arg.id)]["class"]]["range"]
            num_credits_1 = self.class_data[str(
                arg.id)]['unlocked'][self.class_data[str(arg.id)]["class"]]["credits"]

            self.id[ctx.author.id] = True
            self.data[ctx.author.id] = {
                'soldiers': random.randint(num_range_0[0], num_range_0[1]), 'credits': num_credits_0, 'dealt': 0, 'taken': 0, 'ammo': random.randint(1, 3), 'cavalry': False, 'pikeman': False, 'shields': False, 'rage': 0}
            self.data[arg.id] = {
                'soldiers': random.randint(num_range_1[0], num_range_1[0]), 'credits': num_credits_1, 'dealt': 0, 'taken': 0, 'ammo': random.randint(1, 3), 'cavalry': False, 'pikeman': False, 'shields': False, 'rage': 0}
            print(self.data)
            await self.army(ctx)

    @commands.command(aliases=['a'])
    async def accept(self, ctx, arg: discord.Member):
        if self.id[arg.id] == True:
            self.id[ctx.author.id] = {
                'enemy': arg.id, 'enemy_user': arg, 'game': True, 'turn': False}
            self.id[arg.id] = {'enemy': ctx.author.id,
                               'enemy_user': ctx.author, 'game': True, 'turn': True}
            self.game_id = ctx.author.id + arg.id
            self.market[self.game_id] = {
                "light": 5, "heavy": 20, "catapult": 25, "assassin": 10}

            accepted = discord.Embed(
                title="Ready the Army",
                description=f"You have accepted {arg.mention}s War request. Use `.army` to view your army",
                colour=discord.Colour.dark_teal()
            )
            await ctx.send(embed=accepted)
        else:
            await ctx.send("There is nothing to accept")

    async def attack_damage(self, ctx, damage: int) -> int:
        self.data[self.id[ctx.author.id]['enemy']]['soldiers'] -= damage
        self.data[ctx.author.id]['dealt'] += damage
        self.data[self.id[ctx.author.id]['enemy']]['taken'] += damage

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def attack(self, ctx):
        if self.id[ctx.author.id]['turn'] == True:
            if self.data[ctx.author.id]['credits'] >= self.market[self.game_id]['light']:
                damage = random.randint(2, 5)

                self.data[ctx.author.id]['credits'] -= self.market[self.game_id]['light']

                if damage < 4:
                    self.data[ctx.author.id]['rage'] += 1

                self.data[ctx.author.id]['rec'] = False
                await self.attack_damage(ctx, 5)

                print(damage)
                dmg = discord.Embed(
                    title="Light Attack",
                    description=f"""**You killed** `{damage}` enemy soldiers
                                    You have killed a **total** of `{self.data[ctx.author.id]['dealt']}` enemy soldiers""",
                    colour=discord.Colour.orange()
                )
                dmg.set_footer(
                    text=f"You used {self.market[self.game_id]['light']} Credits")
                await ctx.send(embed=dmg)

                await self.turn(ctx)
                await self.death(ctx)
            else:
                await ctx.send("Not enough Credits")
        else:
            await ctx.send("please use the `.war` command to start a battle, or wait your turn")

    @attack.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def heavy(self, ctx):
        if self.id[ctx.author.id]['turn'] == True:
            if self.data[ctx.author.id]['credits'] >= self.market[self.game_id]['heavy']:
                damage = random.randint(6, 9)

                if damage < 7:
                    self.data[ctx.author.id]['rage'] += 1

                await self.attack_damage(ctx, damage)

                self.data[ctx.author.id]['credits'] -= self.market[self.game_id]['heavy']

                dmg = discord.Embed(
                    title="Heavy Attack",
                    description=f"""**You killed** `{damage}` enemy soldiers
                                    You have killed a **total** of `{self.data[ctx.author.id]['dealt']}` enemy soldiers""",
                    colour=discord.Colour.dark_orange()
                )
                dmg.set_footer(
                    text=f"You used {self.market[self.game_id]['heavy']} Credits")
                await ctx.send(embed=dmg)

                await self.turn(ctx)
                await self.death(ctx)
            else:
                await ctx.send("Not enough Credits")

        else:
            await ctx.send("please use the `.war` command to start a battle, or wait your turn")

    @attack.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def assassin(self, ctx, number=1):
        if self.id[ctx.author.id]['turn'] == True:
            if self.data[ctx.author.id]['credits'] >= self.market[self.game_id]['assassin'] * number:
                await self.attack_damage(ctx, number)

                self.data[ctx.author.id]['credits'] -= self.market[self.game_id]['assassin'] * number

                dmg = discord.Embed(
                    title="Assassins in the Dark!",
                    description=f"""**You killed** `{number}` enemy soldiers
                                    You used `{10 * number}` Credits to higher {number} assassins""",
                    colour=discord.Colour.purple()
                )
                dmg.set_footer(
                    text=f"You used {self.market[self.game_id]['assassin']} Credits")
                if number > 1:
                    await self.turn(ctx)

                await ctx.send(embed=dmg)
                await self.death(ctx)
            else:
                await ctx.send("You dont have enough credits")

        else:
            await ctx.send("please use the `.war` command to start a battle, or wait your turn")

    @attack.command()
    async def catapult(self, ctx):
        if self.id[ctx.author.id]['turn'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one, or wait your turn")
        else:
            if self.data[ctx.author.id]['credits'] >= self.market[self.game_id]['catapult']:
                if self.data[ctx.author.id]['ammo'] > 0:
                    self.data[ctx.author.id]['ammo'] -= 1

                    self.data[ctx.author.id]['credits'] -= self.market[self.game_id]['catapult']

                    await self.attack_damage(ctx, 10)
                    dmg = discord.Embed(
                        title=f"Catapults | {self.data[ctx.author.id]['ammo']}",
                        description=f"Youve launched your catapults, you've taken out **10** soldiers",
                        colour=discord.Colour.dark_blue()
                    )
                    dmg.set_footer(
                        text=f"You used {self.market[self.game_id]['catapult']} Credits")
                    await ctx.send(embed=dmg)
                    await self.turn(ctx)
                    await self.death(ctx)
                else:
                    no_ammo = discord.Embed(
                        title="Out of Ammo",
                        description="You dont have enough ammo",
                        colour=discord.Colour.dark_blue()
                    )
                    await ctx.send(embed=no_ammo)
            else:
                ctx.send("Not enough credits")

    @attack.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def surprise(self, ctx):
        if self.id[ctx.author.id]['turn'] == True:
            if self.data[ctx.author.id]['credits'] >= self.market[self.game_id]['surprise']:
                numbers = random.sample(range(10), 4)

                self.data[ctx.author.id]['credits'] -= self.market[self.game_id]['surprise']

                dmg = discord.Embed(
                    title="Surprise Attack",
                    description="You sent a squadron of soldiers to flank the enemy",
                    colour=discord.Colour.gold()
                )
                dmg.add_field(
                    name='Coordinates', value="The coordinates are four differenct numbers ranging from 1 to 10", inline=False)
                dmg.add_field(
                    name='Strength', value="For each coordinate the enemy does not guess you do 3 damage", inline=False)
                dmg.add_field(
                    name='Vulnerabilty', value="For each coordinate the enemy guesses they get 10 credits", inline=False)
                dmg.set_footer(
                    text="opponent has to guess the coordinates ex. `1 4 6 9`")
                dmg.set_footer(
                    text=f"You used {self.market[self.game_id]['surprise']} Credits")
                await ctx.send(embed=dmg)
                await self.turn(ctx)

                msg = []

                def check(m):
                    return m.author == self.id[ctx.author.id]['enemy_user'] and m.channel == ctx.channel

                while True:
                    msg = await self.client.wait_for('message', check=check)
                    msg = list(msg.content)
                    msg = list(filter(lambda x: x != ' ', msg))
                    try:
                        msg = [int(i) for i in msg]
                        break
                    except ValueError:
                        await ctx.send("That is not a valid response")

                print(msg)

                guessed = (len(set(msg).intersection(set(numbers))))
                print(guessed)
                guess = discord.Embed(
                    title="Coordinates",
                    description=f"Your scouts just arrived and told you the coordinates were **{numbers}**",
                    colour=discord.Colour.orange()
                )
                guess.add_field(
                    name='Coordinates', value=f"The coordinates you guessed are **{msg}**", inline=False)
                guess.add_field(
                    name='Earned', value=f"You earned `{10 * guessed}` credits", inline=False)
                guess.add_field(
                    name='Earned', value=f"You took `{(4 - guessed) * 3}` damage", inline=False)

                await ctx.send(embed=guess)
                await self.attack_damage(ctx, (4 - guessed) * 3)
                await self.death(ctx)
            else:
                ctx.send("Not enough credits")
        else:
            await ctx.send("please use the `.war` command to start a battle, or wait your turn")

    ###################################################################################################################################################

    @commands.group(invoke_without_command=True)
    async def rage(self, ctx):
        if self.id[ctx.author.id]['game'] == True:
            rage_help = discord.Embed(
                title="War | Rage",
                description="Use `.rage [type]` to attack in full might",
                colour=discord.Colour.gold()
            )
            rage_help.add_field(
                name='Level', value="Shows your rage level", inline=False)
            rage_help.add_field(
                name='Charge', value="Attack with a garanteed 8 damage", inline=False)
            rage_help.add_field(
                name='mission', value="Attempts to rescue soldiers (6-8)", inline=False)
            await ctx.send(embed=rage_help)

        else:
            await ctx.send("You have not started a battle yet. Use '.war @mention' to start one")

    @rage.command()
    async def level(self, ctx):
        not_full = 6 - self.data[ctx.author.id]['rage']
        full = "■ " * self.data[ctx.author.id]['rage']
        rage_bar = discord.Embed(
            title="Rage Level",
            description=full + "□ " * not_full,
            colour=discord.Colour.dark_red()
        )
        await ctx.send(embed=rage_bar)

    @rage.command()
    async def charge(self, ctx):
        if self.data[ctx.author.id]['rage'] < 3:
            not_rage = discord.Embed(
                title="Not Enough Rage",
                description="You need more rage",
                colour=discord.Colour.greyple()
            )
            await ctx.send(embed=not_rage)

        else:
            await self.attack_damage(ctx, 8)

            rage_dmg = discord.Embed(
                title="Charge!",
                description=f"""You **Destroyed** 8 soldiers
                                You have killed a **total** of `{self.data[ctx.author.id]['dealt']}` enemy soldiers""",
                colour=discord.Colour.dark_red()
            )

            await ctx.send(embed=rage_dmg)
            self.data[ctx.author.id]['rage'] -= 3
            await self.turn(ctx)
            await self.death(ctx)

    @rage.command()
    async def mission(self, ctx):
        if self.data[ctx.author.id]['rage'] < 3:
            not_rage = discord.Embed(
                title="Not Enough Rage",
                description="You need more rage",
                colour=discord.Colour.greyple()
            )
            await ctx.send(embed=not_rage)

        else:
            amount = random.randint(6, 8)
            rescue = discord.Embed(
                title="Rescue",
                description=f"""You rescued {amount}
                                You have a **total** of `{self.data[ctx.author.id]['soldiers']}` soldiers""",
                colour=discord.Colour.dark_red()
            )

            await ctx.send(embed=rescue)
            self.data[ctx.author.id]['rage'] -= 3

    @commands.command()
    async def surrender(self, ctx):
        if self.id[ctx.author.id]['game'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one")
        else:
            del self.data[self.id[ctx.author.id]['enemy']]
            del self.id[self.id[ctx.author.id]['enemy']]
            del self.data[ctx.author.id]
            del self.id[ctx.author.id]

            surrendered = discord.Embed(
                title="Surrender!",
                description=f"It has been an honor fighting with you, ",
                colour=discord.Colour.light_gray()
            )
            surrendered.set_footer(text=ctx.author.name)
            await ctx.send(embed=surrendered)

    @commands.command()
    async def void(self, ctx):
        if self.id[ctx.author.id] == True:
            del self.data[ctx.author.id]
            del self.id[ctx.author.id]

            voided = discord.Embed(
                title="Voided",
                description=f"You have voided this game",
                colour=discord.Colour.light_gray()
            )
            voided.set_footer(text=ctx.author.name)
            await ctx.send(embed=voided)

        elif self.id[ctx.author.id]['game'] == True:
            await ctx.send("You have already started a battle. Use '.surrender' if you want to give up")

        else:
            await ctx.send("You have not started a battle yet. Use '.war' to start one")


def setup(client):
    client.add_cog(Battle(client))
