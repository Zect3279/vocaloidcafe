import discord
from discord.ext import commands
import random
import re
import asyncio

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        
        await ctx.send("https://discord.gg/hUexsMPQmG")
        
    @commands.command()
    async def count(self, ctx):
        
        await ctx.send(ctx.guild.member_count)

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

            msg = f'選出者数: {dice}→{result}'
            for member in members:
                msg += f'\n{member.mention}'
            await ctx.send(msg)
            
    @commands.command()
    async def roulette(self, ctx, number):

        number = int(number)
        members = random.sample(ctx.author.voice.channel.members, number)

        msg = f'選出者数: {number}'
        for member in members:
            msg += f'\n{member.mention}'
        await ctx.send(msg)
        
    @commands.command()
    async def reaction_roulette(self, ctx, number):

        await ctx.message.add_reaction("✅")

        members = []
        def check(reaction, user):
            if reaction.emoji == "✅" and user not in members:
                if user.bot:
                    return
                members.append(user)

        try:
            await self.bot.wait_for("reaction_add", check = check, timeout = 30)
        except asyncio.TimeoutError:
            pass

        number = int(number)
        members = random.sample(members, number)
        
        msg = f'選出者数: {number}'
        for member in members:
            msg += f'\n{member.mention}'
        await ctx.send(msg)

    @commands.command()
    async def ranuta(self, ctx):

        members = ctx.author.voice.channel.members

        random.shuffle(members)

        for member in members:

            if member.display_name.startswith('!'):
                await ctx.send(member.mention)
                break

def setup(bot):
    bot.add_cog(Commands(bot))
