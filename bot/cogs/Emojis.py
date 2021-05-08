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

import re
from typing import Optional

import discord
from discord.ext import commands

from .backend.paginator.paginator import paginator, input
from difflib import get_close_matches
import logging

logger = logging.getLogger("discord")

class Emojis(commands.Cog):
    '''
    Commands related to emojis
    '''
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = ["<:Elite:794608720688185364>"]
        self.cache = {}

    async def updatecache(self):
        async with self.bot.db.pool.acquire() as con:
            emojis = await con.fetch("SELECT * FROM userdata")
        
        tempcache = {}
        for person in emojis:
            tempcache[int(person["user_id"])] = person["emojis"]
        
        self.cache = tempcache
    
    @commands.Cog.listener(name="on_message")
    async def _send_emojis(self, message):
        if not self.cache:
            await self.updatecache()

        if self.cache.get(message.author.id, None) in [True]:
            emojistosend = []
            foundemojinames = re.findall(
                r"((?<=;).+?(?=;))", str(message.content))

            if foundemojinames:
                guildemojinames = {
                    emoji.name.lower(): emoji.name for emoji in message.guild.emojis}
                botemojinames = {
                    emoji.name.lower(): emoji.name for emoji in self.bot.emojis}
                for emojiname in foundemojinames:
                    found = False
                    for emoji in guildemojinames:
                        if emoji == emojiname.lower():
                            foundemoji = discord.utils.get(
                                message.guild.emojis, name=guildemojinames[emoji])
                            found = True
                            break
                    if not found:
                        for emoji in botemojinames:
                            if emoji == emojiname.lower():
                                foundemoji = discord.utils.get(
                                    self.bot.emojis, name=botemojinames[emoji])
                                found = True
                                break
                    if not found:
                        pass
                    else:
                        if foundemoji:
                            if not str(foundemoji) in self.whitelist and foundemoji.available:
                                emojistosend.append(str(foundemoji))

                if emojistosend:
                    if not message.reference:
                        await message.reply(" ".join(emojistosend), mention_author=False)
                    else:
                        msg = await message.channel.fetch_message(message.reference.message_id)
                        for emoji in emojistosend:
                            await msg.add_reaction(emoji)

    @commands.group(name="emojis", aliases=["emoji"], invoke_without_command=True)
    async def _emojis(self, ctx, *, search: Optional[str] = None):
        '''
        Get a list of emojis the bot knows about. Provide optional keyword to search for.
        '''
        if not ctx.invoked_subcommand:
            if not search:
                embeds = []
                emojidict = {emoji.name: emoji for emoji in self.bot.emojis}
                emojis = sorted(list(emojidict))

                emojis = [emojis[n:n+10]
                        for n in range(0, len(emojis), 10)]
                for group in emojis:
                    emojilist = []
                    for emoji in group:
                        if not str(emojidict[emoji]) in self.whitelist and emojidict[emoji].available:
                            emojilist.append(f"{str(emojidict[emoji])} `{emojidict[emoji].name} | {emojidict[emoji].id}`")
                    embed = discord.Embed(description="\n".join(emojilist), colour=self.bot.neutral_embed_colour)
                    embeds.append(input(embed, None))
                
                if embeds:
                    pages = paginator(ctx, remove_reactions=True)
                    pages.add_reaction("\U000023ea", "first")
                    pages.add_reaction("\U000025c0", "back")
                    pages.add_reaction("\U0001f5d1", "delete")
                    pages.add_reaction("\U000025b6", "next")
                    pages.add_reaction("\U000023e9", "last")
                    await pages.send(embeds)
                    
            else:
                embeds = []
                emojidict = {emoji.name: emoji for emoji in self.bot.emojis}
                emojis = sorted(list(emojidict))

                emojis = get_close_matches(search, emojis, len(self.bot.emojis))
                
                emojis = [emojis[n:n+10]
                          for n in range(0, len(emojis), 10)]
                for group in emojis:
                    emojilist = []
                    for emoji in group:
                        if not str(emojidict[emoji]) in self.whitelist and emojidict[emoji].available:
                            emojilist.append(
                                f"{str(emojidict[emoji])} `{emojidict[emoji].name} | {emojidict[emoji].id}`")
                    embed = discord.Embed(description="\n".join(
                        emojilist), colour=self.bot.neutral_embed_colour)
                    embeds.append(input(embed, None))

                if embeds:
                    pages = paginator(ctx, remove_reactions=True)
                    pages.add_reaction("\U000023ea", "first")
                    pages.add_reaction("\U000025c0", "back")
                    pages.add_reaction("\U0001f5d1", "delete")
                    pages.add_reaction("\U000025b6", "next")
                    pages.add_reaction("\U000023e9", "last")
                    await pages.send(embeds)
                else:
                    embed = discord.Embed(title="Error!", description=f"Couldn't find anything matching `{search}`!", colour=self.bot.bad_embed_colour)
                    await ctx.reply(embed=embed, mention_author=False)
    
    @_emojis.command(name="search", aliases=["s"])
    async def _emojis_search(self, ctx, *, search: str):
        '''
        Search for an emoji
        '''
        await self._emojis(ctx, search=search)
    
    @_emojis.command(name="toggle")
    async def _emojis_toggle(self, ctx):
        '''
        Opt in/out of the emoji response
        '''
        async with self.bot.db.pool.acquire() as con:
            emojis = await con.fetch("SELECT emojis FROM userdata WHERE user_id = $1", int(ctx.author.id))
        
        if not len(emojis):
            async with self.bot.db.pool.acquire() as con:
                await con.execute("INSERT INTO userdata values($1, $2)", int(ctx.author.id), True)
                mode = True
        
        else:
            if len(emojis):
                async with self.bot.db.pool.acquire() as con:
                    await con.execute("INSERT INTO userdata values($1, $2) ON CONFLICT (user_id) DO UPDATE SET emojis = $2 where userdata.user_id = $1", int(ctx.author.id), not emojis[0]["emojis"])
                    mode = not emojis[0]["emojis"]
        await self.updatecache()
        embed = discord.Embed(title="Success!", description=f"User emoji response `{'on' if mode else 'off'}`", colour=self.bot.good_embed_colour).set_footer(text=f"You can trigger the emoji any time by doing \";<emojiname>;\"", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, mention_author=False)
        
def setup(bot):
    bot.add_cog(Emojis(bot))
