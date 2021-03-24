import discord
from discord.ext import commands
import asyncio

import r
conn = r.connect()

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def point(self, ctx):

        if len(ctx.message.mentions) > 0:
            member = ctx.message.mentions[0]

            point = conn.zscore('point', member.id)
            await ctx.send(f'{member.mention} {point}')
        else:
            point = conn.zscore('point', ctx.author.id)
            await ctx.send(f'{ctx.author.mention} {point}')

    @commands.command()
    async def send(self, ctx, member: discord.Member):

        conn.zincrby('point', 100, member.id)
        conn.zincrby('point', -100, ctx.author.id)
        await ctx.message.add_reaction('✌️')

    @commands.command()
    async def control(self, ctx, member: discord.Member, number: int):

        if ctx.author.id != 521166149904236554:
            return

        conn.zincrby('point', number, member.id)
        await ctx.message.add_reaction('✌️')

def setup(bot):
    bot.add_cog(Commands(bot))