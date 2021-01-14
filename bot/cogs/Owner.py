import discord
import json
from discord.ext import commands
from cogs.global_functions import get_cogs
import asyncio


initial_cogs = get_cogs()


class Owner(commands.Cog):
    '''Commands just for the owner of the bot'''
    def __init__(self, bot):
        self.bot=bot


    @commands.command(hidden = True, name = "defaultprefix")
    @commands.is_owner()
    async def _defaultprefix(self, ctx, prefix):
        '''Changes the default prefix, can only be used by the bot owner

        Usage
        -----
        defaultprefix <prefix>

        Parameters
        ----------
        prefix: str
            The prefix to change to
        '''

        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes["default"] = str(prefix)

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Default prefix changed to `{prefix}")

    @commands.command(hidden = True, name = "reload")
    @commands.is_owner()
    async def _reload(self, ctx, cog = None):
        if not cog:
            for cogs in initial_cogs:
                try:
                    self.bot.reload_extension(cogs)
                    await ctx.send(f'Reloaded `{cogs}`', delete_after = 10)
                except Exception as e:
                    await ctx.send(f"Error while reloading `{cogs}`: `{e}`")
                await asyncio.sleep(0.5)
            await ctx.send("✅ Successfully reloaded!", delete_after = 10)
        else:
            if cog == "jishaku":
                self.bot.load_extension(cog)
                return await ctx.send(f"Loaded `{cog}`", delete_after = 10)

            if not cog.startswith("cogs."):
                cog = f"cogs.{cog}"
            try:
                self.bot.reload_extension(cog)
                await ctx.send(f"Reloaded `{cog}`", delete_after = 10)
            except Exception as e:
                await ctx.send(f"Error while reloading `{cog}`: `{e}`")

    @commands.command(hidden = True, name = "load")
    @commands.is_owner()
    async def _load(self, ctx, cog = None):
        if not cog:
            for cogs in initial_cogs:
                try:
                    self.bot.load_extension(cogs)
                    await ctx.send(f'Loaded `{cogs}`', delete_after = 10)
                except Exception as e:
                    await ctx.send(f"Error while loading `{cogs}`: `{e}`")
                await asyncio.sleep(0.5)
            await ctx.send("✅ Successfully loaded!", delete_after = 10)
        else:
            if cog == "jishaku":
                self.bot.load_extension(cog)
                return await ctx.send(f"Loaded `{cog}`", delete_after = 10)
            if not cog.startswith("cogs."):
                cog = f"cogs.{cog}"
            try:
                self.bot.load_extension(cog)
                await ctx.send(f"Loaded `{cog}`", delete_after = 10)
            except Exception as e:
                await ctx.send(f"Error while loading `{cog}`: `{e}`")

    @commands.command(hidden = True, name = "unload")
    @commands.is_owner()
    async def _unload(self, ctx, cog = None):
        if not cog:
            for cogs in initial_cogs:
                try:
                    self.bot.unload_extension(cogs)
                    await ctx.send(f'Unloaded `{cogs}`', delete_after = 10)
                except Exception as e:
                    await ctx.send(f"Error while Unloading `{cogs}`: `{e}`")
                await asyncio.sleep(0.5)
            await ctx.send("✅ Successfully Unloaded!", delete_after = 10)
        else:
            if cog == "jishaku":
                self.bot.load_extension(cog)
                return await ctx.send(f"Unloaded `{cog}`", delete_after = 10)

            if not cog.startswith("cogs."):
                cog = f"cogs.{cog}"
            try:
                self.bot.unload_extension(cog)
                await ctx.send(f"Unloaded `{cog}`", delete_after = 10)
            except Exception as e:
                await ctx.send(f"Error while unloading `{cog}`: `{e}`")

    @commands.command(hidden = True, name = "status")
    @commands.is_owner()
    async def _status(self, ctx, status_type, *, message):
        if status_type == "playing":
            activity = discord.Game(message)
        elif status_type == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=message)
        elif status_type == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=message)
        
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.message.add_reaction("👍")

    @commands.command(name = "addcog")
    @commands.is_owner()
    async def _addcog(self, ctx, cog):
        with open("cogs.json", "r") as f:
            cogs = json.load(f)

        if cog.startswith("cogs."):
            if not cog in cogs:
                cogs.append(cog)
            else:
                await ctx.send("Cog has already been added!")
                await ctx.send(f"Added `{cog}`")

                await ctx.invoke(self.bot.get_command("load"), cog = cog)
        else:
            if not f"cogs.{cog}" in cogs:
                cogs.append(f"cogs.{cog}")
                await ctx.send(f"Added `{cog}`")

                await ctx.invoke(self.bot.get_command("load"), cog = cog)
            else:
                await ctx.send("Cog has already been added!")

        cogs.sort()
        
        with open("cogs.json", "w") as f:
            json.dump(cogs, f, indent = 4)


def setup(bot):
    bot.add_cog(Owner(bot))