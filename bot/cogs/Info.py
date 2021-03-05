import discord
from discord.ext import commands
import sys


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def _info(self, ctx):
        '''
        Get info about the bot
        '''
        embed = discord.Embed(
            title="Info", description=f"```\n{self.bot.description}```" if self.bot.description else "", colour=0x2F3136)
        version = sys.version_info
        embed.add_field(name="Python version",
                        value=f"```py\n{version[0]}.{version[1]}.{version[2]}```")
        embed.add_field(name="Discord.py version",
                        value=f"```py\n{discord.__version__}```")
        embed.add_field(
            name="Commands", value=f"```py\n{len(self.bot.commands)}```", inline=True)
        
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
