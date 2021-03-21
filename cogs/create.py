import discord
from discord.ext import commands

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_new(self, guild):

        category = await guild.create_category(name='UNTITLED')
        tc = await category.create_text_channel(name='text-channel')
        vc = await category.create_voice_channel(name='voice-channel')
        await vc.edit(user_limit = 25)

        return tc, vc

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel == before.channel:
            return

        if after.channel is None:
            return

        elif after.channel.id == self.bot.system.create_new_public:
            tc, vc = await self.create_new(member.guild)

            await member.edit(voice_channel=vc)

        elif after.channel.id == self.bot.system.create_new_private:
            tc, vc = await self.create_new(member.guild)

            await tc.set_permissions(member.guild.default_role, read_messages=False)
            await vc.set_permissions(member.guild.default_role, view_channel=False)

            await tc.set_permissions(member, read_messages=True)
            await vc.set_permissions(member, view_channel=True)

            await member.edit(voice_channel=vc)

def setup(bot):
    bot.add_cog(Create(bot))