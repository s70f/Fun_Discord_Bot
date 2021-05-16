from discord.ext import commands
import csv
import random
from random import sample


class Unscramble(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def unscramble(self, ctx):
        file = open('words.txt', 'r')
        reader = csv.reader(file)
        test_list = [row for row in reader]

        res = [''.join(sample(ele, len(ele))) for ele in test_list]

        a = random.choice(res)
        list_word = list(a)
        random.shuffle(list_word)
        print(''.join(list_word))

        await ctx.send('Unscramble ' + '`' + ''.join(list_word) + '`')

        def check(m):
            return m.content == a

        msg = await self.client.wait_for('message', check=check)
        await ctx.send('{.author.mention} has unscrambled It!'.format(msg))


def setup(client):
    client.add_cog(Unscramble(client))
