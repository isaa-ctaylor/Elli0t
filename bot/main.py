import datetime
import json
import os
import random

import discord
import pretty_help
from discord.ext import commands
from dotenv import load_dotenv

from utils.global_functions import get_cogs, get_default_prefix, get_prefix

load_dotenv()

default_prefix = get_default_prefix()

initial_cogs = get_cogs()

description = """
Elli0t is a multi-purpose discord bot aiming to make your life easier. He contains many different modules, spanning moderation, fun and games. Elli0t is open-source and all code can be found on github: (https://github.com/isaa-ctaylor/Elli0t) Any contributions would be welcome!
"""


class Elli0t(discord.ext.commands.AutoShardedBot):
    '''
    A class that inherits from discord.ext.commands.AutoShardedBot
    '''
    async def close(self):
        '''
        Subclass of close, to confirm shutdown
        '''
        await self.change_presence(status = discord.Status.offline, activity=None)
        await super().close()


intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.guilds = True

bot = Elli0t(command_prefix=get_prefix, description=description,
             help_command=pretty_help.PrettyHelp(), intents = intents, case_insensitive = True, activity = discord.Game(name="around while testing"))

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)

bot.start_time = datetime.datetime.utcnow()

@bot.event
async def on_ready():
    '''
    Called when the client is done preparing the data received from Discord. Usually after login is successful and the Client.guilds and co. are filled up.
    '''

    print("Bot is connected to discord.")


bot.run(os.getenv("TOKEN"))
