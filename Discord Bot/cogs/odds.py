import discord as discord
from discord.ext import commands
from discord.ext import tasks
import random
import asyncio


class Odds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def odds(self, ctx, arg1: int, arg2: int):

        # * --- Choosing Number

        number = random.randint(arg1, arg2)
        print(arg1, arg2)
        print(number)

        # * --- Verification

        embed = discord.Embed(
            title='Odds Generator',
            colour=discord.Colour.blue()
        )

        embed.add_field(name='🤔 WARNING',
                        value='`By using the odds generator, you know that if the numbers match, you will be muted for the matched number of minutes.`', inline=False)
        embed.add_field(name='** **',
                        value='`By using the odds generator, you agree that you will not complain if you get muted if the numbers match`', inline=False)
        embed.add_field(
            name='** **', value='If you agree to the statements above, react below.\nIf you do not agree, please do not react.', inline=False)

        embd = await ctx.send(embed=embed)
        await embd.add_reaction('✅')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

        await self.client.wait_for('reaction_add', check=check)

        # * --- Choose Number

        choose = discord.Embed(
            title='Odds Generator',
            description='You may now tell me what number you are choosing',
            colour=discord.Colour.blue()
        )

        choose.add_field(
            name='** **', value='(Please, only type a number.**Do not type `4.` or `four`. Just type `4`)', inline=False)

        await ctx.send(embed=choose)

        channel = ctx.channel

        def check2(m):
            return arg1 <= int(m.content) <= arg2 and m.channel == channel

        choice = await self.client.wait_for('message', check=check2)

        safe = discord.Embed(
            title='Odds Generator',
            description='You are safe!',
            colour=discord.Colour.green()
        )
        safe.add_field(
            name='** **', value=f'The number you chose was `{choice.content}`\nThe number the bot chose was `{number}`', inline=False)

        if int(choice.content) != number:
            await channel.send(embed=safe)

        elif int(choice.content) == number:
            muted = discord.Embed(
                title='Odds Generator',
                description='Oh No! You guessed it correct',
                colour=discord.Colour.red()
            )

            muted.add_field(
                name='** **', value=f'The number you chose was `{choice.content}`\nThe number the bot chose was `{number}`\n**You are muted for `{number}` minutes**', inline=False)

            await channel.send(embed=muted)

            mute_time = number * 60

            member = choice.author

            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.add_roles(role)

            await asyncio.sleep(mute_time)
            await member.remove_roles(role)


def setup(client):
    client.add_cog(Odds(client))
