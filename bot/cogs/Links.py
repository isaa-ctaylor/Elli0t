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


class Links(commands.Cog):
    '''
    A couple helpful links
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="github", aliases=["source", "git", "code"])
    async def _github(self, ctx):
        '''
        Find the source code on github
        '''
        github_embed = discord.Embed(
            title="Github", description=f"Find the source code [here](https://www.github.com/isaa-ctaylor/Elli0t/)")
        github_embed.set_thumbnail(
            url="https://avatars1.githubusercontent.com/u/9919")
        await ctx.reply(embed=github_embed, mention_author=False)

    @commands.command(name="ko-fi", aliases=["coffee", "donate"])
    async def _ko_fi(self, ctx):
        '''
        Buy me a coffee
        '''
        kofi_embed = discord.Embed(
            title="Buy me a coffee", description=f"Click [here](https://ko-fi.com/isaa_ctaylor) to buy me a coffee", colour=self.bot.neutral_embed_colour)
        kofi_embed.set_thumbnail(
            url="https://storage.ko-fi.com/cdn/useruploads/90f7e47d-7c60-4338-b544-dbf2e6196dca.png")
        await ctx.reply(embed=kofi_embed, mention_author=False)

    @commands.command(name="support", aliases=["helpserver"])
    async def _support(self, ctx):
        '''
        Get a link to the support server
        '''
        support_embed = discord.Embed(
            title="Support server", description="Click [here](https://discord.gg/QFmJTNTAry) to join the support server")
        support_embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.reply(embed=support_embed, mention_author=False)

    @commands.command(name="invite")
    async def _invite(self, ctx):
        '''Invite the bot to your server!'''
        embed = discord.Embed(
            title="Invite me!", description="Click [here](https://isaa-ctaylor.github.io/Elli0t/invite/) to add me to your server!")
        await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Links(bot))
