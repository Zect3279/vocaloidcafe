import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        if member.guild.id != 808283612105408533:
            return

        channel = self.bot.get_channel(808302622452613120)
        
        await channel.send(f'{member.mention}\n'\
            'VocaloCaféへようこそ！\n'\
            'はじめに#自己紹介に記入をお願いします♪\n'\
            'VCは誰でも参加して大丈夫です！\n'\
            '気軽に参加してみましょう♪'
        )
        
        role_names = ["Guest"]
        
        for role_name in role_names:
            role = discord.utils.get(member.guild.roles, name = role_name)
            await member.add_roles(role)

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

    @commands.Cog.listener()
    async def on_ready(self):

        channel = self.bot.get_channel(self.bot.system.administrator)
        await channel.send('[LOG]BOTが再起動されました')

def setup(bot):
    bot.add_cog(Admin(bot))