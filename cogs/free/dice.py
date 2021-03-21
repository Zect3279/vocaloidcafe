import discord
from discord.ext import commands
import random
import re

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """nDn検知時に自動でダイスロール"""
        
        info = re.fullmatch(r"(\d+)d(\d+)", message.content)
        if info is not None:
            
            result = 0
            number = int(info.group(1))
            size = int(info.group(2))

            if number > 10000 or size > 10000:
                return await message.channel.send('数値が大きすぎます')

            for i in range(number):
                result += random.randint(1, size)

            await message.channel.send(f'🎲{result}')

def setup(bot):
    bot.add_cog(Dice(bot))