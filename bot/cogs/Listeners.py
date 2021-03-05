import discord
from discord.ext import commands
import logging
import traceback

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.logger=logging.getLogger("discord")

    @commands.Cog.listener(name="on_command")
    async def _log_command_invoke(self, ctx):
        self.logger.info(
            f"Command \"{ctx.command.name}\" started by {ctx.author.name}#{ctx.author.discriminator} in guild {ctx.guild.name}")

    @commands.Cog.listener(name="on_command_completion")
    async def _log_command_completion(self, ctx):
        self.logger.info(
            f"Command \"{ctx.command.name}\" finished successfully. {ctx.author.name}#{ctx.author.discriminator} in guild {ctx.guild.name}")

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
            error_embed = discord.Embed(title="Error!", description=str(
                error), colour=discord.Colour.red())
            await ctx.reply(embed=error_embed)

        elif isinstance(error, commands.errors.TooManyArguments):
            pass

        elif isinstance(error, discord.errors.HTTPException):
            return
            await ctx.reply("There was an error, please try again later. If you are trying to message someone, they might have it turned off.")

        elif isinstance(error, discord.errors.NotFound):
            pass

        elif isinstance(error, commands.errors.MissingPermissions):
            perms = ", ".join(error.missing_perms)
            error_embed = discord.Embed(
                title="Error!", description=f"You are missing the following perm(s): `{perms}`", colour=discord.Colour.red())
            await ctx.reply(embed=error_embed)

        elif isinstance(error, commands.errors.BotMissingPermissions):
            perms = ", ".join(error.missing_perms)
            error_embed = discord.Embed(
                title="Error!", description=f"I am missing the following perm(s): `{perms}`", colour=discord.Colour.red())
            await ctx.reply(embed=error_embed)

        elif isinstance(error, discord.errors.Forbidden):
            await ctx.reply("I couldn't do that, sorry. Try checking my perms")

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            param = str(error.param).split(":")[0]
            error_embed = discord.Embed(
                title="Error!", description=f"Missing parameter: `{param}`", colour=discord.Colour.red())
            await ctx.reply(embed=error_embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error!", description="You need to be owner to execute this command!", colour=discord.Colour.red())
            await ctx.send(embed=embed)

        else:
            error_embed = discord.Embed(
                title="Error!", description=f"```diff\n- {str(error)}```\nIf this keeps happening, please contact `isaa_ctaylor#2494`", colour=discord.Colour.red())
            
            tb = "".join(traceback.format_exception(
                type(error), error, error.__traceback__))
            
            self.logger.error(
                f"Command error!\nCommand name: {ctx.command.qualified_name}, Author: {ctx.author.name}#{ctx.author.discriminator}\n{tb}")
            
            await ctx.reply(embed=error_embed)
            
    @commands.Cog.listener(name="on_message_edit")
    async def _reinvoke_commands(self, before, after):
        if after.content != before.content:
            await self.bot.process_commands(after)
            
def setup(bot):
    bot.add_cog(Listeners(bot))
