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

import os
import difflib
from dotenv import load_dotenv

import discord
from discord.ext import commands
from jishaku.functools import executor_function
import json
import aiohttp
from discord.ext.commands.cooldowns import BucketType

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "../blacklist.json")

load_dotenv()

class Owner(commands.Cog):
    '''
    Commands just for the owner of the bot
    '''

    def __init__(self, bot):
        self.bot = bot
        self.cogs = bot.loaded_cogs
        self.whitelist = [
            "jishaku"
        ]

    def _trusted_check(ctx):
        if ctx.author.id in [718087881087910018, 589156304841605121]:
            return True
        raise commands.NotOwner("You must be owner to use this command!")
    
    async def load_cog(self, cog: str) -> discord.Embed:

        try:
            self.bot.load_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Loaded `{cog}`", colour=self.bot.good_embed_colour)
            if cog not in self.cogs:
                if cog in self.whitelist or cog.startswith("cogs."):
                    self.cogs.append(cog)
                else:
                    self.cogs.append(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error loading `{cog}`: `{e}`", colour=self.bot.bad_embed_colour)
        finally:
            return embed

    async def reload_cog(self, cog: str) -> discord.Embed:
        try:
            self.bot.reload_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Reloaded `{cog}`", colour=self.bot.good_embed_colour)
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error reloading `{cog}`: `{e}`", colour=self.bot.bad_embed_colour)
        finally:
            self.cogs.sort()
            return embed
    
    async def unload_cog(self, cog: str) -> discord.Embed:
        try:
            self.bot.unload_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Unloaded `{cog}`", colour=self.bot.good_embed_colour)
            if cog in self.cogs:
                if cog in self.whitelist or cog.startswith("cogs."):
                    self.cogs.pop(self.cogs.index(cog))
                else:
                    self.cogs.pop(
                        self.cogs.index(f"cogs.{cog}"))
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error unloading `{cog}`: `{e}`", colour=self.bot.bad_embed_colour)
        finally:
            self.cogs.sort()
            return embed

    @commands.is_owner()
    @commands.command(name="load")
    async def _load(self, ctx: commands.Context, *, cog: str):
        '''
        Load the given cog
        '''
        if cog not in self.whitelist and not cog.startswith("cogs."):
            cog = [f'cogs.{str(e).split(".")[0]}' for e in list(
                difflib.get_close_matches(cog, os.listdir(dirname), n=1))][0]

        await ctx.send(embed=await self.load_cog(cog))

    @commands.is_owner()
    @commands.command(name="reload")
    async def _reload(self, ctx: commands.Context, *, cog: str = None):
        '''
        Reload the given cog
        '''
        if cog:
            if cog in self.whitelist or cog.startswith("cogs."):
                await ctx.send(embed=await self.reload_cog(cog))
            else:
                await ctx.send(embed=await self.reload_cog(f"cogs.{cog}"))
        else:
            cogs = []
            good = 0
            bad = 0

            for i, cog in enumerate(self.cogs):
                try:
                    self.bot.reload_extension(cog)
                    cogs.append(f"<:greenTick:813679271620771870> `{cog}`")
                    good += 1
                except Exception as e:
                    cogs.append(
                        f"<:redCross:813679325114794014>`{cog}`: `{e}`")
                    bad += 1

            colour = self.bot.good_embed_colour if good >= bad else self.bot.bad_embed_colour
            cogs = "\n".join(cogs)

            embed = discord.Embed(title="Reloaded all cogs",
                                  description=cogs, colour=colour)
            await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="unload")
    async def _unload(self, ctx, *, cog):
        if cog in self.whitelist or cog.startswith("cogs."):
            await ctx.send(embed=await self.unload_cog(cog))
        else:
            await ctx.send(embed=await self.unload_cog(f"cogs.{cog}"))

    @commands.is_owner()
    @commands.command(name="prefixless")
    async def _prefixless(self, ctx, onoroff: str = None):
        if str(onoroff).lower() in ["true", "yes", "1", "on"]:
            self.bot.prefixless = True
            await ctx.message.add_reaction("👍")
        elif str(onoroff).lower() in ["false", "no", "0", "off"]:
            self.bot.prefixless = False
            await ctx.message.add_reaction("👍")
        elif not onoroff:
            self.bot.prefixless = not self.bot.prefixless
            await ctx.message.add_reaction("👍")

    @commands.is_owner()        
    @commands.command(name="restart")
    async def _restart(self, ctx):
        await ctx.send(embed=discord.Embed(title="Restarting", description="Be back soon!", colour=self.bot.good_embed_colour))
        await self.bot.close()

    @executor_function
    def _do_blacklist(self, user, reason):
        with open(filename, "r") as f:
            data = json.load(f)
        
        if not data.get(str(user), None):
            data[str(user)] = reason or "None specified"
            self.bot.blacklist[str(user)] = reason or "None specified"
        else:
            del data[str(user)]
            del self.bot.blacklist[str(user)]
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    
    @commands.is_owner()
    @commands.command(name="blacklist")
    async def _blacklist(self, ctx, user: discord.User, *, reason: str = None):
        if user.id != self.bot.owner_id:
            await self._do_blacklist(user.id, reason)
            return await ctx.message.add_reaction("\U0001f44d")
        return await ctx.message.add_reaction("\U0000274c")

    @commands.cooldown(1, 60, BucketType.user)
    @commands.check(_trusted_check)
    @commands.command(name="cdn")
    async def _cdn(self, ctx):
        with ctx.typing():
            if ctx.message.attachments:
                if not ctx.message.attachments[0].size > 99614720:
                    imgbytes = await ctx.message.attachments[0].read()
                    async with aiohttp.ClientSession() as cs:
                        async with cs.post("https://isaac.likes-throwing.rocks/upload", data={"image": imgbytes, "token": os.getenv("sxcu"), "noembed": "True", "og_properties": '{"discord_hide_url": "True"}'}) as r:
                            readdata = await r.json()

                    embed = discord.Embed(description=f'[`{readdata["url"]}`]({readdata["url"]})', colour=self.bot.good_embed_colour)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("too big smh")
            else:
                await ctx.send("hmm")

def setup(bot):
    bot.add_cog(Owner(bot))
