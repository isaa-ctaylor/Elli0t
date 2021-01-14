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
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            error_embed = discord.Embed(title = "Error!", description = error, colour = discord.Colour.red())
            await ctx.send(embed = error_embed)

        elif isinstance(error, discord.errors.HTTPException):
            await ctx.send("There was an error, please try again later. If you are trying to message someone, they might have it turned off.")

        elif isinstance(error, discord.errors.NotFound):
            pass

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the correct permissions to do that!")

        elif isinstance(error, discord.Forbidden):
            await ctx.send("I couldn't do that, sorry. Try checking my perms")

        else:
            await ctx.send("An internal error occured, if this keeps happening, please contact `isaa_ctaylor#2494`")
            
            tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))

            await self.bot.get_user(self.bot.owner_id).send(f"Error!\nAuthor: `{ctx.author.name}#{ctx.author.discriminator}`\nGuild: `{ctx.guild.name}`, `{ctx.guild.id}`\nCommand: {ctx.command}\nCog: {ctx.cog}\nTraceback:\n```py\n{tb}\n```")
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    '''
    Adds the cog
    '''
    bot.add_cog(Errors(bot))
