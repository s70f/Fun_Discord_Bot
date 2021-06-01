import discord as discord
from discord.ext import commands
import random
import time


class Battle(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data = {}
        self.id = {}
        
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send("please dont spam")

    async def turn(self, ctx):
            self.id[self.id[ctx.author.id]['enemy']]['turn'] = True
            self.id[ctx.author.id]['turn'] = False

    async def death(self, ctx):
        if self.data[ctx.author.id]['soldiers'] <= 0:
            dead = discord.Embed(
                title="Dead!",
                description=f"It has been an honor fighting with you",
                colour=discord.Colour.dark_red()
            )
            await ctx.send(embed=dead)
    
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
            print(ctx.author)
            army.add_field(
                name=f"Army Name", value=f"🔺 {ctx.author.display_name}'s Army", inline=False)
            army.add_field(
                name='Soldiers', value=f"🍢 {self.data[ctx.author.id]['soldiers']}", inline=False)
            army.add_field(
                name='Catapult Ammo', value=f"💣 {self.data[ctx.author.id]['ammo']}", inline=False)
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
        if ctx.author.id not in self.id.keys():
            await ctx.send("You have not started a battle yet. Use '.war' to start one")
        else:

            arg = self.id[ctx.author.id]['enemy_user']
            
            enemy = discord.Embed(
                # title="Bot's Army",
                colour=discord.Colour.red()
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
                name='Cavalry', value=self.data[arg.id]['cavalry'], inline=False)
            enemy.add_field(
                name='Pikeman', value=self.data[arg.id]['pikeman'], inline=False)
            enemy.add_field(
                name='Shields', value=self.data[arg.id]['shields'], inline=False)
            enemy.add_field(
                name='Damage Dealt', value=f"🔸 {self.data[arg.id]['dealt']}", inline=False)
            enemy.add_field(
                name='Damage Taken', value=f"🔹 {self.data[arg.id]['taken']}", inline=False)
            
            await ctx.send(embed=enemy)

    @commands.command()
    async def war(self, ctx, arg : discord.Member):
        if ctx.author.id in self.id.keys():
            await ctx.send('You have already started a battle')
        else:
            self.id[ctx.author.id] = True

            self.data[ctx.author.id] = {
                'soldiers': random.randint(25, 40), 'dealt': 0, 'taken': 0, 'ammo': random.randint(1, 3), 'cavalry': False, 'pikeman': False, 'shields': False, 'rec': False}
            self.data[arg.id] = {
                'soldiers': random.randint(25, 40), 'dealt': 0, 'taken': 0, 'ammo': random.randint(1, 3), 'cavalry': False, 'pikeman': False, 'shields': False, 'rec': False}

            await self.army(ctx)
    
    @commands.command()
    async def accept(self, ctx, arg : discord.Member):
        if self.id[arg.id] == True:
            self.id[ctx.author.id] = {'enemy': arg.id, 'enemy_user': arg, 'game': True, 'turn': False}
            self.id[arg.id] = {'enemy': ctx.author.id, 'enemy_user': ctx.author, 'game': True, 'turn': True}  
            print(self.id)
            
            accepted = discord.Embed(
                title="Ready the Army",
                description=f"You have accepted {arg.mention}s War request. Use `.army` to view your army",
                colour=discord.Colour.dark_red()
            )
            await ctx.send(embed=accepted)
        else:
            await ctx.send("There is nothing to accept")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def attack(self, ctx):
        if self.id[ctx.author.id]['turn'] == True:
            damage = random.randint(3, 6)
            print(damage)
            if self.data[ctx.author.id]['cavalry'] == True: 
                damage += 2
            elif self.data[ctx.author.id]['pikeman'] == True:
                damage -= 2
            elif self.data[ctx.author.id]['rec'] == True:
                damage -= 1
                self.self.data[ctx.author.id]['rec'] = False
                #TODO: Change recruitment

            self.data[self.id[ctx.author.id]['enemy']]['soldiers'] -= damage
            self.data[ctx.author.id]['dealt'] += damage
            self.data[self.id[ctx.author.id]['enemy']]['taken'] += damage
            print(self.data)
            dmg = discord.Embed(
                title="Attack!",
                description=f"""**You killed** `{damage}` enemy soldiers
                                You have killed a **total** of `{self.data[ctx.author.id]['dealt']}` enemy soldiers""",
                colour=discord.Colour.orange()
            )

            await self.turn(ctx)
            await ctx.send(embed=dmg)
            await self.death(ctx)

        else:
            await ctx.send("please use the `.war` command to start a battle, or wait your turn")

    @commands.group(invoke_without_command=True)
    async def enable(self, ctx):
        if self.id[ctx.author.id]['game'] == True:
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
                name='Shields', value=f"Enables Shields: sacrifices men from maining the catapults to hold 5 shields (-5 attack damage once and -1 ammo)", inline=False)
            await ctx.send(embed=enable_help)
            await self.turn(ctx)
        else:
            await ctx.send("You have not started a battle yet. Use '.war @mention' to start one")

    @enable.command()
    async def cavalry(self, ctx): 
        if self.id[ctx.author.id]['turn'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one, or wait your turn")
        else:
            self.data[ctx.author.id]['cavalry'] = True
            self.data[ctx.author.id]['soldiers'] -= 10

            cavalry_enable = discord.Embed(
                    title="War | Cavalry Enabled",
                    description="Enables Cavalry: guaranteed +2 attack damage on every attack but sells 10 of your soldiers for horses",
                    colour=discord.Colour.purple()
                )

            await ctx.send(embed=cavalry_enable)
            await self.turn(ctx)
    
    @enable.command()
    async def pikeman(self, ctx):
        if self.id[ctx.author.id]['turn'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one, or wait your turn")
        else:
            self.data[ctx.author.id]['pikeman'] = True
            self.data[ctx.author.id]['soldiers'] += 10

            pikeman_enable = discord.Embed(
                    title="War | Pikeman Enabled",
                    description="Enables Pikeman: +10 soldiers but -2 damage on every attack",
                    colour=discord.Colour.purple()
                )

            await ctx.send(embed=pikeman_enable)
            await self.turn(ctx)

    @enable.command()
    async def shields(self, ctx):
        if self.id[ctx.author.id]['turn'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one, or wait your turn")
        else:
            if self.data[ctx.author.id]['ammo'] > 0:
                self.data[ctx.author.id]['shields'] = True
                self.data[ctx.author.id]['ammo'] -= 1

                shields_enable = discord.Embed( 
                        title="War | Shields Enabled",
                        description="Enables Shields: sacrifices men from maining the catapults to hold 5 shields (-5 attack damage once and -1 ammo)",
                        colour=discord.Colour.purple()
                    )

                await ctx.send(embed=shields_enable)
                await self.turn(ctx)
            else:
                shields_disabled = discord.Embed(
                        title="War | Shields Disabled",
                        description="You dont have enough men",
                        colour=discord.Colour.purple()
                    )

                await ctx.send(embed=shields_disabled)
                
    
    @commands.command()
    async def catapult(self, ctx):
        if self.id[ctx.author.id]['turn'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one, or wait your turn")
        else:
            if self.data[ctx.author.id]['ammo'] > 0:
                damage = random.randint(5, 8)
                self.data[ctx.author.id]['ammo'] -= 1
                self.data[self.id[ctx.author.id]['enemy']]['soldiers'] -= damage
                self.data[ctx.author.id]['dealt'] += damage
                self.data[self.id[ctx.author.id]['enemy']]['taken'] += damage
                catapult_attack = discord.Embed(
                    title=f"Catapults | {self.data[ctx.author.id]['ammo']}",
                    description=f"Youve launched your catapults, you've taken out **{damage}** soldiers",
                    colour=discord.Colour.dark_blue()
                )
                await ctx.send(embed=catapult_attack)
                await self.turn(ctx)
                await self.death(self, ctx)
            else:
                no_ammo = discord.Embed(
                    title="Out of Ammo",
                    description="You dont have enough ammo",
                    colour=discord.Colour.dark_blue()
                )
                await ctx.send(embed=no_ammo)
    
    @commands.command()
    async def recruit(self, ctx):
        if self.id[ctx.author.id]['turn'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one, or wait your turn")
        else:
            number = random.randint(4, 6)
            self.self.data[ctx.author.id]['rec'] = True
            self.data[ctx.author.id]['soldiers'] += number
            recruitement = discord.Embed(
                    title="Recruitement",
                    description=f"you have recruited {number} Soldiers from a nearby village, untrained soldiers will do -1 damage on first attack",
                    colour=discord.Colour.dark_blue()
                )
            await ctx.send(embed=recruitement)

    @commands.command()
    async def surrender(self, ctx):
        if self.id[ctx.author.id]['game'] == False:
            await ctx.send("You have not started a battle yet. Use '.war' to start one")
        else:
            del self.id[self.id[ctx.author.id]['enemy']]
            del self.id[ctx.author.id]
            del self.data[self.id[ctx.author.id]['enemy']]
            del self.data[ctx.author.id]
            surrendered = discord.Embed(
                title="Surrender!",
                description=f"It has been an honor fighting with you, ",
                colour=discord.Colour.light_gray()
            )
            await ctx.send(embed=surrendered)

def setup(client):
    client.add_cog(Battle(client))
