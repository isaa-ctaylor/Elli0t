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

class Settings(commands.Cog):
    '''
    Settings for your guild
    '''
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix = None):
        '''
        Change the prefix for your server
        '''
        if not prefix:
            return await ctx.embed(title="Prefix", description=f"The prefix for this guild is currently `{self.bot.get_prefix(ctx.message)}`")
        
        oldprefix = ctx.prefix
        
        self.bot = await self.bot.db.setPrefix(self.bot, ctx.guild.id, prefix)
        
        await ctx.guild.me.edit(nick = f"[{prefix}] {ctx.guild.me.display_name.removeprefix(f'[{oldprefix}] ')}")
        
        success_embed = discord.Embed(title = "Success!", description = f"Prefix changed to `{prefix}`", colour = self.bot.good_embed_colour)
        await ctx.reply(embed = success_embed)
        

def setup(bot):
    bot.add_cog(Settings(bot))
