from discord.ext import commands

async def get_prefix(bot, message):
    '''
    Returns the prefix for the given guild
    '''
    if (message.author.id in bot.owner_ids) and bot.prefixless:
        return commands.when_mentioned_or(["", str(bot.prefixes[int(message.guild.id)])])
    return commands.when_mentioned_or(bot.prefixes[int(message.guild.id)])(bot, message)