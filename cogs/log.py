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

        free_room = self.bot.get_channel(808307478470459412)

        if before.channel is not None:
            if before.channel.category == free_room:
                channel = discord.utils.get(free_room.text_channels, name = before.channel.name)
                embed = discord.Embed(description = f'{member.mention}さんが退室しました')
                msg = await channel.send(embed = embed)
                await asyncio.sleep(5)
                await msg.delete()
                
        if after.channel is not None:
            if after.channel.category == free_room:
                channel = discord.utils.get(free_room.text_channels, name = after.channel.name)
                embed = discord.Embed(description = f'{member.mention}さんが入室しました')
                msg = await channel.send(embed = embed)
                await asyncio.sleep(5)
                await msg.delete()
  
def setup(bot):
    bot.add_cog(Log(bot))
