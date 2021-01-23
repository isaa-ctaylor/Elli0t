import discord
from discord.ext import commands
import asyncio
import json
from utils.global_functions import get_default_prefix, timeInSeconds
import random
import datetime
import translate
import langdetect
import html

default_prefix = get_default_prefix()

class Utility(commands.Cog):
    '''All the commands in here are like your utility belt!'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases = ["pong"])
    async def _ping(self, ctx):
        '''
        Table tennis anyone?
        '''
        if ctx.invoked_with.lower() == "ping":
            title = "Pong 🏓"
        else:
            title = "Ping 🏓"
        embed = discord.Embed(
            title = title, description=f"Latency = `{round(self.bot.latency * 1000, 2)}ms`", colour = random.randint(0x000000, 0xFFFFFF))

        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Utility(bot))
