import discord
from discord.ext import commands

import asyncio

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel == before.channel:
            return

        if after.channel is None:
            return

        if after.channel.name != 'voice-channel':
            return

        category = after.channel.category

        channel = discord.utils.get(category.channels, name = 'text-channel')
        embed = discord.Embed(description = f'{member.mention} さんが入室しました')
        msg = await channel.send(embed=embed)

        await asyncio.sleep(5)

        await msg.delete()

def setup(bot):
    bot.add_cog(Log(bot))