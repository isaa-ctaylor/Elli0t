import asyncio
import sys
import traceback

import discord
from discord.ext import commands


class Errors(commands.Cog):
    '''
    An error handler
    '''
    def __init__(self, bot):
        self.bot=bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        The default command error handler provided by the bot.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog

        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.errors.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.reply(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.errors.BadArgument):
            error_embed = discord.Embed(title = "Error!", description = str(error), colour = discord.Colour.red())
            await ctx.reply(embed = error_embed)
        
        elif isinstance(error, commands.errors.TooManyArguments):
            pass
        
        elif isinstance(error, discord.errors.HTTPException):
            return
            await ctx.reply("There was an error, please try again later. If you are trying to message someone, they might have it turned off.")

        elif isinstance(error, discord.errors.NotFound):
            pass

        elif isinstance(error, commands.errors.MissingPermissions):
            perms = ", ".join(error.missing_perms)
            error_embed = discord.Embed(title = "Error!", description = f"You are missing the following perm(s): `{perms}`", colour = discord.Colour.red())
            await ctx.reply(embed = error_embed)

        elif isinstance(error, commands.errors.BotMissingPermissions):
            perms = ", ".join(error.missing_perms)
            error_embed = discord.Embed(title = "Error!", description = f"I am missing the following perm(s): `{perms}`", colour = discord.Colour.red())
            await ctx.reply(embed = error_embed)

        elif isinstance(error, discord.errors.Forbidden):
            await ctx.reply("I couldn't do that, sorry. Try checking my perms")
            
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            param = str(error.param).split(":")[0]
            error_embed = discord.Embed(title = "Error!", description = f"Missing parameter: `{param}`", colour = discord.Colour.red())
            await ctx.reply(embed = error_embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Error!", description="You need to be owner to execute this command!", colour=discord.Colour.red())
            await ctx.send(embed=embed)
            
        else:
            error_embed = discord.Embed(title = "Error!", description = f"Error type: {type(error)}\nError message: {str(error)}\nIf this keeps happening, please contact `isaa_ctaylor#2494`", colour=discord.Colour.red())
            await ctx.reply(embed = error_embed)
            
            tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))

            try:
                await (await self.bot.fetch_user(self.bot.owner_id)).send(f"Error!\nAuthor: `{ctx.author.name}#{ctx.author.discriminator}`\nGuild: `{ctx.guild.name}`, `{ctx.guild.id}`\nCommand: {ctx.command}\nCog: {ctx.cog}\nTraceback:\n```py\n{tb}\n```")
            except:
                print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    '''
    Adds the cog
    '''
    bot.add_cog(Errors(bot))
