import asyncio
import json
import os

import discord
from discord.ext import commands

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "../json/data.json")


class Owner(commands.Cog):
    '''Commands just for the owner of the bot'''

    def __init__(self, bot):
        self.bot = bot
        self.cogs = bot.loaded_cogs
        self.whitelist = [
            "jishaku"
        ]

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    async def load_cog(self, bot, cog) -> discord.Embed:
        try:
            bot.load_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Loaded `{cog}`", colour=discord.Colour.green())
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error loading `{cog}`: `{e}`", colour=discord.Colour.red())
        finally:
            return embed

    async def reload_cog(self, bot, cog) -> discord.Embed:
        try:
            bot.reload_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Reloaded `{cog}`", colour=discord.Colour.green())
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error reloading `{cog}`: `{e}`", colour=discord.Colour.red())
        finally:
            return embed
        
    async def unload_cog(self, bot, cog) -> discord.Embed:
        try:
            bot.unload_extension(cog)
            embed = discord.Embed(
                title="Success!", description=f"Unloaded `{cog}`", colour=discord.Colour.green())
        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"Error unloading `{cog}`: `{e}`", colour=discord.Colour.red())
        finally:
            return embed

    @commands.command(name="load")
    async def _load(self, ctx, *, cog):
        '''
        Load the given cog
        '''
        if cog in self.whitelist:
            await ctx.send(embed=await self.load_cog(self.bot, cog))
            if not cog in self.bot.loaded_cogs:
                self.bot.loaded_cogs.append(cog)
        elif cog.startswith("cogs."):
            await ctx.send(embed=await self.load_cog(self.bot, cog))
            if not cog in self.bot.loaded_cogs:
                self.bot.loaded_cogs.append(cog)
        else:
            await ctx.send(embed=await self.load_cog(self.bot, f"cogs.{cog}"))
            if not cog in self.bot.loaded_cogs:
                self.bot.loaded_cogs.append(f"cogs.{cog}")

    @commands.command(name="reload")
    async def _reload(self, ctx, *, cog=None):
        '''
        Reload the given cog
        '''
        if cog:
            if cog in self.whitelist:
                await ctx.send(embed=await self.reload_cog(self.bot, cog))
            elif cog.startswith("cogs."):
                await ctx.send(embed=await self.reload_cog(self.bot, cog))
            else:
                await ctx.send(embed=await self.reload_cog(self.bot, f"cogs.{cog}"))
        else:
            cogs = []
            good = 0
            bad = 0
            
            for i, cog in enumerate(self.bot.loaded_cogs):
                try:
                    self.bot.reload_extension(cog)
                    cogs.append(f"<:greenTick:596576670815879169> `{cog}`")
                    good += 1
                except Exception as e:
                    cogs.append(
                        f"<:redTick:596576672149667840> `{cog}`: `{e}`")
                    bad += 1

            if good >= bad:
                colour = discord.Colour.green()
            else:
                colour = discord.Colour.red()

            cogs = "\n".join(cogs)

            embed = discord.Embed(title="Reloaded all cogs",
                                  description=cogs, colour=colour)
            await ctx.send(embed=embed)
            
    @commands.command(name="unload")
    async def _unload(self, ctx, *, cog):
        if cog in self.whitelist:
            await ctx.send(embed=await self.unload_cog(self.bot, cog))
            if cog in self.bot.loaded_cogs:
                self.bot.loaded_cogs.pop(self.bot.loaded_cogs.index(cog))
        elif cog.startswith("cogs."):
            await ctx.send(embed=await self.unload_cog(self.bot, cog))
            if cog in self.bot.loaded_cogs:
                self.bot.loaded_cogs.pop(self.bot.loaded_cogs.index(cog))
        else:
            await ctx.send(embed=await self.unload_cog(self.bot, f"cogs.{cog}"))
            if cog in self.bot.loaded_cogs:
                self.bot.loaded_cogs.pop(self.bot.loaded_cogs.index(f"cogs.{cog}"))

    @_load.error
    @_reload.error
    @_unload.error
    async def _NotOwner(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CheckFailure):
            error_embed = discord.Embed(title="Error!", description="You need to be owner to use this command!", colour=discord.Colour.red())
            await ctx.send(embed=error_embed)
            
def setup(bot):
    bot.add_cog(Owner(bot))
