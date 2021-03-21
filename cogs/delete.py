import discord
from discord.ext import commands

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel == before.channel:
            return

        if before.channel is None:
            return

        if before.channel.name != 'voice-channel':
            return

        if len(before.channel.members) == 0:
            category = before.channel.category
            for channel in category.channels:
                await channel.delete()
            await category.delete()

def setup(bot):
    bot.add_cog(Delete(bot))