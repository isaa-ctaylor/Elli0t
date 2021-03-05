import asyncio
import json
import os
import difflib

import discord
from discord.ext import commands

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, ".")


class Owner(commands.Cog):
    '''Commands just for the owner of the bot'''

    def __init__(self, bot):
        self.bot = bot
        self.cogs = bot.loaded_cogs
        self.whitelist = [
            "jishaku"
        ]

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    async def load_cog(self, cog: str) -> discord.Embed:

        try:
            self.bot.load_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Loaded `{cog}`", colour=discord.Colour.green())
            if cog not in self.cogs:
                if cog in self.whitelist or cog.startswith("cogs."):
                    self.cogs.append(cog)
                else:
                    self.cogs.append(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error loading `{cog}`: `{e}`", colour=discord.Colour.red())
        finally:
            return embed

    async def reload_cog(self, cog: str) -> discord.Embed:
        try:
            self.bot.reload_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Reloaded `{cog}`", colour=discord.Colour.green())
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error reloading `{cog}`: `{e}`", colour=discord.Colour.red())
        finally:
            self.cogs.sort()
            return embed

    async def unload_cog(self, cog: str) -> discord.Embed:
        try:
            self.bot.unload_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Unloaded `{cog}`", colour=discord.Colour.green())
            if cog in self.cogs:
                if cog in self.whitelist or cog.startswith("cogs."):
                    self.cogs.pop(self.cogs.index(cog))
                else:
                    self.cogs.pop(
                        self.cogs.index(f"cogs.{cog}"))
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error unloading `{cog}`: `{e}`", colour=discord.Colour.red())
        finally:
            self.cogs.sort()
            return embed

    @commands.command(name="load")
    async def _load(self, ctx: commands.Context, *, cog: str):
        '''
        Load the given cog
        '''
        if cog not in self.whitelist and not cog.startswith("cogs."):
            cog = [f'cogs.{str(e).split(".")[0]}' for e in list(
                difflib.get_close_matches(cog, os.listdir(dirname), n=1))][0]

        await ctx.send(embed=await self.load_cog(cog))

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

            colour = discord.Colour.green() if good >= bad else discord.Colour.red()
            cogs = "\n".join(cogs)

            embed = discord.Embed(title="Reloaded all cogs",
                                  description=cogs, colour=colour)
            await ctx.send(embed=embed)

    @commands.command(name="unload")
    async def _unload(self, ctx, *, cog):
        if cog in self.whitelist or cog.startswith("cogs."):
            await ctx.send(embed=await self.unload_cog(cog))
        else:
            await ctx.send(embed=await self.unload_cog(f"cogs.{cog}"))

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
            
    @commands.command(name="restart")
    async def _restart(self, ctx):
        await ctx.send(embed=discord.Embed(title="Restarting", description="Be back soon!", colour=discord.Colour.green()))
        await self.bot.close()

    @_load.error
    @_reload.error
    @_unload.error
    @_restart.error
    async def _NotOwner(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CheckFailure):
            error_embed = discord.Embed(
                title="Error!", description="You need to be owner to use this command!", colour=discord.Colour.red())
            await ctx.send(embed=error_embed)


def setup(bot):
    bot.add_cog(Owner(bot))
