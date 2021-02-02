import datetime
import json
import os
import random

import asyncio
import aiohttp
import discord
import pretty_help
from discord.ext import commands
from dotenv import load_dotenv

from utils.utils import get_prefix, updatePrefixes

load_dotenv()

default_prefix = "-"

description = """
Elli0t is a multi-purpose discord bot aiming to make your life easier. He contains many different modules, spanning moderation, fun and games. Elli0t is open-source and all code can be found on github: https://github.com/isaa-ctaylor/Elli0t Any contributions would be welcome!
"""

intents = discord.Intents.all()

start_time = datetime.datetime.utcnow()
session = aiohttp.ClientSession()

class Elli0t(discord.ext.commands.AutoShardedBot):
    '''
    A class that inherits from discord.ext.commands.AutoShardedBot
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

        self.start_time = kwargs.pop("start_time")
        self.session = kwargs.pop("session")
        self.loaded_cogs = kwargs.pop("cogs")

    async def close(self):
        '''
        Subclass of close, to confirm shutdown
        '''
        await self.session.close()
        await self.change_presence(status=discord.Status.offline, activity=None)
        await super().close()

async def load_cogs(bot):
    for cog in bot.loaded_cogs:
        try:
            bot.load_extension(cog)
            print(f"Loaded {cog}")
        except Exception as e:
            print(e)

bot = Elli0t(
    command_prefix=get_prefix,
    description=description,
    help_command=pretty_help.PrettyHelp(),
    intents=intents,
    case_insensitive=True,
    activity=discord.Game(name="around while testing"),
    start_time=start_time,
    session=session,
    cogs=[
        "cogs.AutoSetup",
        "cogs.Links",
        "cogs.Moderation",
        "cogs.Owner",
        "cogs.Errors",
        "cogs.Images",
        "cogs.Chatbot",
        "jishaku"
    ]
)

bot = bot.run_until_complete(updatePrefixes(bot))

bot.run_until_complete(load_cogs(bot))

@bot.event
async def on_ready():
    '''
    Called when the client is done preparing the data received from Discord. Usually after login is successful and the Client.guilds and co. are filled up.
    '''

    print("Bot is connected to discord.")


bot.run(os.getenv("TOKEN"))