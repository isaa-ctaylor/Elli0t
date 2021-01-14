import json
import os
import random

import discord
from discord.ext import commands
import pretty_help
from discord.ext import commands
from dotenv import load_dotenv

from cogs.global_functions import get_cogs, get_default_prefix

load_dotenv()

default_prefix = get_default_prefix()

initial_cogs = get_cogs()

description = """Elli0t is a multi-purpose Discord bot aimed at making your life easier!
Elli0t contains many modules such as modules for moderation, a ticketing system, music playing and general fun too!"""

# create a class that inherits from discord.ext.commands.Bot
class Elli0t(discord.ext.commands.AutoShardedBot):
    async def close(self):  # subclass close()
        print("\nConnection safely closed.")  # prints to confirm shutdown
        await self.change_presence(status = discord.Status.offline, activity = None)
        await super().close()  # calls the super of close() to properly shut down


# define a function to get custom prefix for each server, called in the definition of `bot`
def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:  # opens prefixes.json
        prefixes = json.load(f)  # loads prefixes.json to a python dictionary

    # returns the prefix for that server
    return prefixes[str(message.guild.id)]

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = Elli0t(command_prefix = get_prefix, description=description,
             help_command=pretty_help.PrettyHelp(), intents = intents, case_insensitive = True)

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)


@bot.event
async def on_ready():
    '''Called when the client is done preparing the data received from Discord. Usually after login is successful and the Client.guilds and co. are filled up.
    '''

    print("Bot is connected to discord.")


bot.run(os.getenv("TOKEN"))
