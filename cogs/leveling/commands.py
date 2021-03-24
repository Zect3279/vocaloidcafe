import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
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
    async def send(self, ctx, member: discord.Member, number: int):

        point = conn.zscore("point", ctx.author.id)

        if point < number:
            return

        if number < 0:
            return

        conn.zincrby('point', number, member.id)
        conn.zincrby('point', -1 * number, ctx.author.id)
        await ctx.message.add_reaction('✌️')

    @cog_ext.cog_slash(
        name = "send",
        description = "メンバーにポイントを送信します",
        guild_ids = [808283612105408533],
        options = [
            create_option(
                name = "target",
                description = "送信先",
                option_type = 6,
                required = True
            ),
            create_option(
                name = "number",
                description = "送信ポイント数",
                option_type = 4,
                required = True
            )
        ]
    )
    async def _send(self, ctx: SlashContext, target: discord.User, number: int):

        await ctx.respond()

        point = conn.zscore("point", ctx.author.id)

        if point < number:
            return

        if number < 0:
            return

        conn.zincrby('point', number, target.id)
        conn.zincrby('point', -1 * number, ctx.author.id)
        
        embed = discord.Embed(description=f'{ctx.author.mention}が{target.mention}に{number}ポイント送金しました')
        await ctx.send(embed = embed)

    @commands.command()
    async def ranking(self, ctx):

        rank = conn.zrevrange('point', 0, 10, withscores=True)
        msg = ''
        for r in rank:
            user = self.bot.get_user(int(r[0]))
            msg += f'{r[1]} {user.mention}\n'

        embed = discord.Embed(description=msg)
        await ctx.send(ctx.author.mention ,embed = embed)

    @commands.command()
    async def control(self, ctx, member: discord.Member, number: int):

        if ctx.author.id != 521166149904236554:
            return

        conn.zincrby('point', number, member.id)
        await ctx.message.add_reaction('✌️')

    @commands.command()
    async def voicechat_control(self, ctx, number: int):

        if ctx.author.id != 521166149904236554:
            return

        for member in ctx.author.voice.channel.members:

            conn.zincrby('point', number, member.id)
            await ctx.message.add_reaction('✌️')

    @commands.command()
    async def login_bonus(self, ctx):
        
        if ctx.author.id != 521166149904236554:
            return
        
        conn.delete('login')

def setup(bot):
    bot.add_cog(Commands(bot))