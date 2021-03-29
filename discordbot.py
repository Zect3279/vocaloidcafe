import discord
from discord.ext import commands
from discord_slash import SlashCommand
import settings

from cogs.utils.system import System

token = settings.TOKEN
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
slash = SlashCommand(bot, sync_commands=True)

bot.system = System()

cogs = [
    'cogs.create',
    'cogs.delete',
    'cogs.log',
    'cogs.commands',
    'cogs.admin',
    'cogs.free.commands',
    'cogs.free.dice'
#     'cogs.leveling.point',
#     'cogs.leveling.commands',
#     'cogs.minigame.hitblow',
#     'cogs.minigame.highlow',
#     'cogs.minigame.doubleup'
]

for cog in cogs:
    bot.load_extension(cog)

bot.run(token)
