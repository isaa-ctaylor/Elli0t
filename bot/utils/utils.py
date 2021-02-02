import json
import discord
from discord.ext import commands
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "../json/data.json")

async def updatePrefixes(bot):
    bot.prefixes = {}
    
    with open(filename, "r") as f:
        data = json.load(f)

    bot.prefixes["default"] = data["defaults"]["prefix"]

    for i in data["servers"]:
        bot.prefixes[str(i)] = str(data["servers"][str(i)]["prefix"])
        
    return bot

async def get_prefix(bot, message):
    '''
    Returns the prefix for the given guild
    '''
    return commands.when_mentioned_or(bot.prefixes[str(message.guild.id)])(bot, message)


async def get_default_prefix(bot):
    return bot.prefixes[str("default")]

async def setPrefix(bot, guild_id, prefix):
    with open(filename, "r") as f:
        data = json.load(f)
        
    data["servers"][str(guild_id)]["prefix"] = str(prefix)
    
    with open(filename, "w") as f:
        json.dump(data, f, indent = 4)
    
    return await updatePrefixes(bot)