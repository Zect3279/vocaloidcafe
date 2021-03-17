import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
slash = SlashCommand(bot, sync_commands = True)

cogs = [
    'cogs.system',
    'cogs.log',
    'cogs.free.commands',
    'cogs.free.dice'
]
for cog in cogs:
    bot.load_extension(cog)

bot.run(os.environ['DISCORD_BOT_TOKEN'])
