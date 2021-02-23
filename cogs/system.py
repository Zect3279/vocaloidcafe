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

        chat = self.bot.get_channel(808313939636125766)
        free_room = self.bot.get_channel(808307478470459412)

        if after.channel is not None:
            if after.channel.category == chat:
                if len(after.channel.members) == 1:
                    channel = await chat.create_text_channel(name = after.channel.name)
                    role = discord.utils.get(member.guild.roles, name = "@everyone")
                    await channel.set_permissions(role, read_messages = False)
                    await channel.set_permissions(member, read_messages = True)
                else:
                    channel = discord.utils.get(member.guild.text_channels, name = after.channel.name)
                    await channel.set_permissions(member, read_messages = True)
            if after.channel.category == free_room:
                channel = discord.utils.get(free_room.text_channels, name = after.channel.name)
                await channel.send(f'{member.mention}さんが入室しました')
                
        if before.channel is not None:
            if before.channel.category == chat:
                channel = discord.utils.get(chat.text_channels, name = before.channel.name)
                await channel.set_permissions(member, read_messages = False)
                if len(before.channel.members) == 0:
                    await channel.delete()
                    
    @commands.command()
    async def admin(self, ctx):

        if ctx.author.id != 521166149904236554:
            return

        role = discord.utils.get(ctx.guild.roles, name = "Admin")
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send("管理者が剥奪されました")
        else:
            await ctx.author.add_roles(role)
            await ctx.send("管理者が付与されました")

def setup(bot):
    bot.add_cog(System(bot))
