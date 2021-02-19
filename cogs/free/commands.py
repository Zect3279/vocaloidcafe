import discord
from discord.ext import commands
import random
import re

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        
        await ctx.send("https://discord.gg/hUexsMPQmG")
        
    @commands.command()
    async def count(self, ctx):
        
        await ctx.send(ctx.guild.member_count)
        
    @commands.command()
    async def roulette(self, ctx):

        members = ctx.author.voice.channel.members
        member = random.choice(members)
        await ctx.send(member.mention)

    @commands.command()
    async def dice_roulette(self, ctx, dice):

        info = re.fullmatch(r"(\d+)d(\d+)", dice)
        if info is not None:
            
            result = 0
            number = int(info.group(1))
            size = int(info.group(2))

            if number > 10000 or size > 10000:
                return await ctx.send('数値が大きすぎます')

            for i in range(number):
                result += random.randint(1, size)

            members = random.sample(ctx.author.voice.channel.members, result)

            msg = f'今日の布教会の当選者を発表します！\n当選者数: {dice} → {result}'
            for member in members:
                msg += f'\n{member.mention}'
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(Dice(bot))