import discord
from discord.ext import commands
import random
import re

import r
conn = r.connect()

class Hitblow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def du(self, ctx):
        
        point = conn.zscore("point", ctx.author.id)

        if point < 100:
            await ctx.send('お金を貯めてからもう一度お願いします')
            return

        conn.zincrby('point', -100, ctx.author.id)
        bet = 100

        while True:

            msg = await ctx.send(f'{bet} 左右のどちらかを選択してください')
            await msg.add_reaction('⏮️')
            await msg.add_reaction('⏭️')

            def check(reaction, user):
                if user.id != ctx.author.id:
                    return
                if reaction.message.channel != ctx.channel:
                    return
                if reaction.emoji in ['⏮️', '⏭️']:
                    return True

            await self.bot.wait_for('reaction_add', check=check)

            if random.randint(0, 1) == 0:
                msg = await ctx.send('正解 賭け金が倍になりました\nダブルアップを続行する YES or NO')
                bet *= 2
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
                    await ctx.send('お疲れ様でした')
                    conn.zincrby('point', bet, ctx.author.id)
                    break

            else:
                await ctx.send('不正解 賭け金を失いました')
                break
                  

def setup(bot):
    bot.add_cog(Hitblow(bot))
