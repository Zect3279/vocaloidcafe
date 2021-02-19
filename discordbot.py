import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

cogs = [
    'cogs.system',
    'cogs.free.commands',
    'cogs.free.dice'
]
for cog in cogs:
    bot.load_extension(cog)

bot.run(os.environ['DISCORD_BOT_TOKEN'])
