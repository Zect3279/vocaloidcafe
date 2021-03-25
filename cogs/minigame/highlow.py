import discord
from discord.ext import commands
import random
import re

import r
conn = r.connect()

class Highlow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duc(self, ctx):

        point = conn.zscore("point", ctx.author.id)

        if point < 100:
            await ctx.send('```賭け金を貯めてからもう一度お願いします```')
            return

        conn.zincrby('point', -100, ctx.author.id)
        bet = 100

        await ctx.send(f'```1から13まであるトランプのカードが\n自分と相手に1枚ずつ配られました```')

        while True:

            you = random.randint(1, 13)
            me = random.randint(1, 13)

            msg = await ctx.send(f'```相手のカードは {you} でした\n自分のカードを予想してください```')
            await msg.add_reaction('⤴️')
            await msg.add_reaction('⤵️')

            def check(reaction, user):
                if user.id != ctx.author.id:
                    return
                if reaction.message.channel != ctx.channel:
                    return
                if reaction.emoji in ['⤴️', '⤵️']:
                    return True

            reaction, user = await self.bot.wait_for('reaction_add', check=check)

            if reaction.emoji == '⤴️' and me > you or reaction.emoji == '⤵️' and me < you:
                mag = (7 - abs(7 - you)) / 7 + 1
                msg = await ctx.send(f'```正解 {int(bet)} -> {int(bet * mag)}\n続行しますか?```')
                bet *= mag

                await msg.add_reaction('⭕')
                await msg.add_reaction('❌')

                def check2(reaction, user):
                    if user.id != ctx.author.id:
                        return
                    if reaction.message.channel != ctx.channel:
                        return
                    if reaction.emoji in ['⭕', '❌']:
                        return True

                reaction, user = await self.bot.wait_for('reaction_add', check=check2)

                if reaction.emoji == '⭕':
                    pass
                else:
                    await ctx.send(f'お疲れ様でした\n{int(bet)}ポイントの返金です')
                    conn.zincrby('point', int(bet), ctx.author.id)
                    break

            else:
                await ctx.send('不正解 賭け金を全て失いました')
                break

def setup(bot):
    bot.add_cog(Highlow(bot))