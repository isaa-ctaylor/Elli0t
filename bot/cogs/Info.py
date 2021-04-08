"""
MIT License

Copyright (c) 2021 isaa-ctaylor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands
import sys


class Info(commands.Cog):
    '''
    Info commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def _info(self, ctx):
        '''
        Get info about the bot
        '''
        embed = discord.Embed(
            title="Info", description=f"```\n{self.bot.description}```" if self.bot.description else "", colour=self.bot.neutral_embed_colour)
        version = sys.version_info
        embed.add_field(name="Python version",
                        value=f"```py\n{version[0]}.{version[1]}.{version[2]}```")
        embed.add_field(name="Discord.py version",
                        value=f"```py\n{discord.__version__}```")
        embed.add_field(name="Server count",
                        value=f"```py\n{len(self.bot.guilds)}```")
        embed.add_field(name="Member count",
                        value=f"```py\n{len(self.bot.users)}```")
        embed.add_field(
            name="Commands", value=f"```py\n{len(self.bot.commands)}```", inline=True)
        
        
        await ctx.reply(embed=embed, mention_author=False)
        
    @commands.command(name="guildinfo")
    async def _guildinfo(self, ctx):
        '''
        Get info about the current guild
        '''
        embed = discord.Embed(title=ctx.guild.name, colour=self.bot.neutral_embed_colour)
        if guild.icon:
            embed.set_thumbnail(url=str(ctx.guild.icon_url))
        embed.add_field(name="Members", value=f"```yaml\nTotal: {sum([1 for member in ctx.guild.members])}\nHumans: {sum([1 for member in ctx.guild.members if not member.bot])}\nBots: {sum([1 for member in ctx.guild.members if member.bot])}```")
        if ctx.guild.features:
            features = "\n".join([f"<:greenTick:596576670815879169> {feature.replace('_', ' ').capitalize()}" for feature in sorted(ctx.guild.features)])
            embed.add_field(name="Features", value=f"{features}")
        embed.add_field(name="Boosting", )
        
        await ctx.reply(embed=embed, mention_author=False)
    
    


def setup(bot):
    bot.add_cog(Info(bot))
