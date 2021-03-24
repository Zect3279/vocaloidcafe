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
    async def hb(self, ctx):

        digit = 4 # 解の桁数

        l = list(range(10)) # 0~9の配列を用意
        random.shuffle(l) # 配列をシャッフル
        solution = [str(n) for n in l[:digit]] # 配列から桁数分取り出し文字列に変換

        turn = 0
        await ctx.send('Gamestart!!')

        while True:

            turn += 1 # ターンを進める

            def check(msg):
                if msg.author != ctx.author:
                    return
                if msg.channel != ctx.channel:
                    return
                if msg.content == 'reset':
                    return True
                if re.fullmatch(r"[0-9]{4}", msg.content) is None: # マッチを確認
                    return
                return True

            msg = await self.bot.wait_for('message', check = check)
            if msg.content == 'reset':
                await ctx.send(solution)
                break
            expected = list(msg.content)

            hitBlow = [0, 0]

            # HitとBlowを確認
            for i in range(digit):
                if expected[i] == solution[i]:
                    hitBlow[0] += 1
                elif expected[i] in solution:
                    hitBlow[1] += 1

            # 正解の場合と不正解の場合
            if hitBlow[0] == digit: 
                await ctx.send(f'Congratulations!! TURN:{turn}')
                conn.zincrby('point', 100, ctx.author.id)
                break
            else:
                await ctx.send(f'HIT:{hitBlow[0]}, BLOW:{hitBlow[1]}')

def setup(bot):
    bot.add_cog(Hitblow(bot))
