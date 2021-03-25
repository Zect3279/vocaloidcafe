import discord
from discord.ext import commands
import asyncio
import datetime
import schedule
import time

import r
conn = r.connect()

class Point(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        conn.zincrby('point', 10, message.author.id)

        l = conn.lrange("login", 0, -1)
        if str(message.author.id) not in l:
            conn.rpush("login", message.author.id)

            conn.zincrby('point', 1000, message.author.id)
            await message.add_reaction('🥳')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            return

        conn.zincrby('point', 3, payload.member.id)

    @commands.Cog.listener()
    async def on_ready(self):

        while True:

            guild = self.bot.get_guild(808283612105408533)
            members = []

            for channel in guild.voice_channels:
                members.extend(channel.members)

            for member in members:
                if member.voice.self_mute == True:
                    conn.zincrby('point', 200, member.id)
                    await ch.send(f'200 {member.id}')
                elif member.voice.self_mute == False:
                    conn.zincrby('point', 300, member.id)
                    await ch.send(f'300 {member.id}')
                    
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(Point(bot))
