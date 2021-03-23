import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def voicechat_list(self, ctx):

        msg = ''

        for channel in ctx.guild.text_channels:
            if channel.name != 'text-channel':
                return
            msg += f'{channel.mention} {channel.category.name}({len(channel.category.voice_channels[0].members)})'

        await ctx.send(msg)

    @cog_ext.cog_slash(
        name = "rename",
        description = "カテゴリの名前を変更します",
        guild_ids = [808283612105408533],
        options = [
            create_option(
                name = "name",
                description = "変更後のカテゴリ名",
                option_type = 3,
                required = True
            )
        ]
    )
    async def _rename(self, ctx: SlashContext, name: str):

        await ctx.respond()

        if ctx.channel.name != 'text-channel':
            return

        category = ctx.channel.category

        await category.edit(name=name)
        await ctx.send(f'カテゴリ名を {name} に変更しました')

    @cog_ext.cog_slash(
        name = "invite",
        description = "チャンネルにメンバーを追加します",
        guild_ids = [808283612105408533],
        options = [
            create_option(
                name = "member",
                description = "追加するメンバー",
                option_type = 6,
                required = True
            )
        ]
    )
    async def _invite(self, ctx: SlashContext, member: discord.User):

        await ctx.respond()

        if ctx.channel.name != 'text-channel':
            return

        category = ctx.channel.category

        tc = discord.utils.get(category.text_channels, name='text-channel')
        vc = discord.utils.get(category.voice_channels, name='voice-channel')

        await tc.set_permissions(member, read_messages = True)
        await vc.set_permissions(member, view_channel = True)

        await ctx.send(f'{member.mention} を追加しました')

def setup(bot):
    bot.add_cog(Commands(bot))
