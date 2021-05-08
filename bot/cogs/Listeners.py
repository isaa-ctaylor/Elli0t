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

import logging
import traceback
from difflib import get_close_matches
from collections import Counter

import discord
from discord.ext import commands
from discord.mentions import AllowedMentions

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.logger=logging.getLogger("discord")
        self.bot.add_check(self._check_not_blacklisted)
        


    @commands.Cog.listener(name="on_command")
    async def _log_command_invoke(self, ctx):
        self.logger.info(
            f"Command \"{ctx.command.name}\" started by {ctx.author.name}#{ctx.author.discriminator} in guild {ctx.guild.name}")

    @commands.Cog.listener(name="on_command_completion")
    async def _log_command_completion(self, ctx):
        try:
            self.bot.command_counter
        except:
            self.bot.command_counter = Counter()
        self.bot.command_counter.update([str(ctx.command.name)])
        self.logger.info(
            f"Command \"{ctx.command.name}\" finished successfully. {ctx.author.name}#{ctx.author.discriminator} in guild {ctx.guild.name}")

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     """
    #     The default command error handler provided by the bot.
    #     """
    #     if hasattr(ctx.command, 'on_error'):
    #         return

    #     cog = ctx.cog

    #     if cog:
    #         if cog._get_overridden_method(cog.cog_command_error) is not None:
    #             return

    #     ignored = ()
    #     error = getattr(error, 'original', error)

    #     if isinstance(error, ignored):
    #         return
        
    #     # if isinstance(error, Blacklisted):
    #     #     return await ctx.error(f"Sorry! You are blacklisted for reason: {error.reason}", reply=True)
        
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.error(f"This command is on cooldown. Try again in {int(error.retry_after)}.")
        
    #     if isinstance(error, commands.ConversionError):
    #         await ctx.error(f"Failed to convert {error.original} to type {error.converter.__name__}")
        
    #     if isinstance(error, commands.CommandNotFound):
    #         thecommands = [command.name for command in self.bot.commands if not command.hidden and command]

    #         matches = get_close_matches(ctx.invoked_with, thecommands)
            
    #         if matches:
    #             embed = discord.Embed(title="Error!", description=f"I couldn't find that command!\nMaybe you meant `{ctx.prefix}{matches[0]}`?", colour=self.bot.bad_embed_colour)
    #             await ctx.reply(embed=embed, mention_author=False)
            
            
    #     if isinstance(error, commands.DisabledCommand):
    #         await ctx.reply(f'{ctx.command} has been disabled.')

    #     elif isinstance(error, commands.NoPrivateMessage):
    #         try:
    #             await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
    #         except discord.HTTPException:
    #             pass

    #     elif isinstance(error, commands.errors.BadArgument):
    #         if str(error).strip().startswith("Converting to \""):
    #             to = str(error).split('"')[1].strip()
    #             param = str(error).split('"')[3].strip()
    #             return await ctx.error(f"Failed to convert the parameter passed for {param} to type {to}. Check {ctx.prefix}help {ctx.invoked_with} for more info.", reply=True)
    #         else:
    #             return await ctx.error(str(error), reply=True)

    #     elif isinstance(error, commands.errors.TooManyArguments):
    #         pass

    #     elif isinstance(error, discord.errors.HTTPException):
    #         return
    #         await ctx.reply("There was an error, please try again later. If you are trying to message someone, they might have it turned off.")

    #     elif isinstance(error, discord.errors.NotFound):
    #         pass

    #     elif isinstance(error, commands.errors.MissingPermissions):
    #         perms = ", ".join(error.missing_perms)
    #         error_embed = discord.Embed(
    #             title="Error!", description=f"You are missing the following perm(s): `{perms}`", colour=self.bot.bad_embed_colour)
    #         await ctx.reply(embed=error_embed)

    #     elif isinstance(error, commands.errors.BotMissingPermissions):
    #         perms = ", ".join(error.missing_perms)
    #         error_embed = discord.Embed(
    #             title="Error!", description=f"I am missing the following perm(s): `{perms}`", colour=self.bot.bad_embed_colour)
    #         await ctx.reply(embed=error_embed)

    #     elif isinstance(error, discord.errors.Forbidden):
    #         await ctx.reply("I couldn't do that, sorry. Try checking my perms")

    #     elif isinstance(error, commands.errors.MissingRequiredArgument):
    #         param = str(error.param).split(":")[0]
    #         error_embed = discord.Embed(
    #             title="Error!", description=f"Missing parameter: `{param}`", colour=self.bot.bad_embed_colour)
    #         await ctx.reply(embed=error_embed)

    #     elif isinstance(error, commands.NotOwner):
    #         embed = discord.Embed(
    #             title="Error!", description="You need to be owner to execute this command!", colour=self.bot.bad_embed_colour)
    #         await ctx.reply(embed=embed, mention_author=False)

    #     else:
    #         error_embed = discord.Embed(
    #             title="Error!", description=f"{type(error)}```diff\n- {str(error)}```\nIf this keeps happening, please contact `isaa_ctaylor#2494`", colour=self.bot.bad_embed_colour)
            
    #         tb = "".join(traceback.format_exception(
    #             type(error), error, error.__traceback__))
            
    #         self.logger.error(
    #             f"Command error!\nCommand name: {ctx.command.qualified_name}, Author: {ctx.author.name}#{ctx.author.discriminator}\n{tb}")
            
    #         await ctx.reply(embed=error_embed)
            
    @commands.Cog.listener(name="on_message_edit")
    async def _reinvoke_commands(self, before, after):
        if after.content != before.content:
            await self.bot.process_commands(after)
            
    @commands.Cog.listener(name="on_message")
    async def _send_prefix(self, message):
        if message.content in [str(self.bot.user.mention), "<@!778637164388810762>"]:
            await ctx.embed(title="Hey there!", description=f"The prefix for this server is `{self.bot.prefixes[message.guild.id]}` or {message.guild.me.mention}!", colour=self.bot.neutral_embed_colour)

    @commands.Cog.listener(name="on_message")
    async def _check_afk(self, message):
        try:
            self.bot.afk
        except AttributeError:
            self.bot.afk = {}
            return

        for afk in self.bot.afk:
            user = await self.bot.fetch_user(afk)
            if user.mentioned_in(message) and not message.author.id == afk:
                await message.reply(f"Hey there {message.author.mention}! Sorry to bother you, but {user} is afk! Reason: `{self.bot.afk[afk].reason or 'None specified'}`", mention_author=False, allowed_mentions=AllowedMentions.none())
        
        if message.author.id in self.bot.afk and not self.bot.afk[message.author.id].messageid == message.id:
            del self.bot.afk[message.author.id]
            await message.reply(f"Welcome back {message.author.mention}! I have removed your afk status.", mention_author=False, allowed_mentions=AllowedMentions.none())
    
    @commands.Cog.listener(name="on_guild_join")
    async def _set_prefix_in_db(self, guild):
        channel = await (await self.bot.fetch_guild(799581511937425468)).fetch_channel(839200251347730473)
        await channel.send("test")
    
    async def _check_not_blacklisted(self, ctx):
        if not str(ctx.author.id) in list(self.bot.blacklist):
            return True
    
def setup(bot):
    bot.add_cog(Listeners(bot))
