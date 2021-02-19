import discord
from discord.ext import commands
import random

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_main_channel(self, message):
        channel = self.bot.get_channel(808302622452613120)
        await channel.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.send_main_channel('Botが再起動されました')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        if member.guild.id != 808283612105408533:
            return 
        
        await self.send_main_channel(
            f'{member.mention}\n'\
            'VocaloCaféへようこそ！\n'\
            'はじめに#自己紹介に記入をしてください♪\n'\
            'VCは誰でも参加して大丈夫です！\n'\
            '気軽に参加してみましょう♪'
        )
        
        role_names = ["Guest", "DJ"]
        
        for role_name in role_names:
            role = discord.utils.get(member.guild.roles, name = role_name)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel == before.channel:
            return

        category = self.bot.get_channel(808313939636125766)

        if after.channel is not None:
            if after.channel.category == category:
                if len(after.channel.members) == 1:
                    channel = await category.create_text_channel(name = after.channel.name)
                    role = discord.utils.get(member.guild.roles, name = "@everyone")
                    await channel.set_permissions(role, read_messages = False)
                await channel.set_permissions(member, read_messages = True)
                
        if before.channel is not None:
            if before.channel.category == category:
                channel = discord.utils.get(category.text_channels, name = before.channel.name)
                await channel.set_permissions(member, read_messages = False)
                if len(before.channel.members) == 0:
                    channel = discord.utils.get(member.guild.text_channels, name = before.channel.name)
                    await channel.delete()

def setup(bot):
    bot.add_cog(System(bot))
