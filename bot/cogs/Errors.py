import discord
from discord.ext import commands
import datetime as dt
import humanize as humanise
import traceback as tb

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name="on_command_error")
    async def _handle_errors(self, ctx, error):
        try:
            if hasattr(ctx.command, "on_error"):
                return
            
            cog = ctx.cog
            
            if cog:
                if cog.has_error_handler():
                    return
                
            ignored = (commands.CommandNotFound, )
            
            error = getattr(error, "original", error)
            
            if isinstance(error, ignored):
                return
            
            elif isinstance(error, commands.MissingRequiredArgument):
                return await ctx.error(f"Whoops! Looks like you missed the {error.param} parameter!", reply=True)
            
            elif isinstance(error, commands.PrivateMessageOnly):
                return await ctx.error("This command can only be used in a private message!", reply=True)
            
            elif isinstance(error, commands.NoPrivateMessage):
                return await ctx.error("This command cannot be used in a private message!", reply=True)
            
            elif isinstance(error, commands.DisabledCommand):
                return await ctx.error("This command is currently disabled! Sorry!", reply=True)
            
            elif isinstance(error, commands.TooManyArguments):
                return await ctx.error(f"Too many arguments passed to {ctx.invoked_with}", reply=True)
            
            elif isinstance(error, commands.CommandOnCooldown):
                return await ctx.error(f"You are on cooldown! Try again in {humanise.precisedelta(dt.timedelta(seconds=error.retry_after))}", reply=True)
            
            elif isinstance(error, commands.MaxConcurrencyReached):
                return await ctx.error(f"This command has reached maximum concurrency!", reply=True)
            
            elif isinstance(error, commands.NotOwner):
                return await ctx.error("You need to be owner to execute this command!", reply=True)
            
            elif isinstance(error, commands.MessageNotFound):
                return await ctx.error(f"Couldn't find the message {error.argument}!", reply=True)
            
            elif isinstance(error, commands.MemberNotFound):
                return await ctx.error(f"Couldn't find the member {error.argument}!", reply=True)
            
            elif isinstance(error, commands.GuildNotFound):
                return await ctx.error(f"Couldn't find the guild {error.argument}!", reply=True)
            
            elif isinstance(error, commands.UserNotFound):
                return await ctx.error(f"Couldn't find the user {error.argument}!", reply=True)
            
            elif isinstance(error, commands.ChannelNotFound):
                return await ctx.error(f"Couldn't find the channel {error.argument}!", reply=True)
            
            elif isinstance(error, commands.ChannelNotReadable):
                return await ctx.error(f"I can't read the channel {error.argument.name}!", reply=True)
            
            elif isinstance(error, commands.BadColourArgument):
                return await ctx.error(f"Unrecognised colour {error.argument}", reply=True)
            
            elif isinstance(error, commands.RoleNotFound):
                return await ctx.error(f"Couldn't find the role {error.argument}!", reply=True)
            
            elif isinstance(error, commands.BadInviteArgument):
                return await ctx.error(f"That invite is invalid or expired!", reply=True)
            
            elif isinstance(error, commands.EmojiNotFound):
                return await ctx.error(f"Couldn't find the emoji {error.argument}!", reply=True)
            
            elif isinstance(error, commands.PartialEmojiConversionFailure):
                return await ctx.error(f"Invalid emoji {error.argument}!", reply=True)
            
            elif isinstance(error, commands.BadBoolArgument):
                return await ctx.error(f"Invalid bool argument!", reply=True)
            
            elif isinstance(error, commands.MissingPermissions):
                return await ctx.error(f"You are missing the following permissions: {', '.join([permission.replace('_', ' ').capitalize() for permission in error.missing_perms])}", reply=True)
            
            elif isinstance(error, commands.BotMissingPermissions):
                return await ctx.error(f"I am missing the following permissions: {', '.join([permission.replace('_', ' ').capitalize() for permission in error.missing_perms])}", reply=True)
            
            elif isinstance(error, commands.MissingRole):
                return await ctx.error(f"You dont have the role {error.missing_role if isinstance(role, str) else (await ctx.guild.fetch_role(error.missing_role)).name}!", reply=True)
            
            elif isinstance(error, commands.BotMissingRole):
                return await ctx.error(f"I dont have the role {error.missing_role if isinstance(role, str) else (await ctx.guild.fetch_role(error.missing_role)).name}!", reply=True)
            
            elif isinstance(error, commands.MissingAnyRole):
                missing_roles = ", ".join([((await ctx.guild.fetch_role(role)).name if ctx.guild.get_role(role) == None else ctx.guild.get_role(role)) if isinstance(role, int) else role for role in error.missing_roles])
                return await ctx.error(f"You are missing the following roles: {missing_roles}!", reply=True)

            elif isinstance(error, commands.BotMissingAnyRole):
                missing_roles = ", ".join([((await ctx.guild.fetch_role(role)).name if ctx.guild.get_role(role) == None else ctx.guild.get_role(role)) if isinstance(role, int) else role for role in error.missing_roles])
                return await ctx.error(f"I am missing the following roles: {missing_roles}!", reply=True)
            
            elif isinstance(error, commands.NSFWChannelRequired):
                return await ctx.error(f"The channel \"{error.channel.name}\" needs to be marked NSFW!", reply=True)
            
            else:
                await ctx.error("Oh... Didn't see that one coming! Sorry, an unexpected error has occurred. This has been logged and will be fixed soon! Sorry for the inconvenience!", reply=True)
                
                async with self.bot.db.pool.acquire() as con:
                    await con.execute("INSERT INTO errors(command, user_id, guild_id, traceback, shorterror) VALUES($1, $2, $3, $4, $5)", ctx.command.qualified_name, ctx.author.id, ctx.guild.id, "".join(tb.format_exception(type(error), error, error.__traceback__)), str(error))

                return await ctx.embed(destination=await ctx.isaac(), title="Error!", description="A new error has arrived!", colour=self.bot.bad_embed_colour)
        except Exception as e:
            await ctx.error(str(e))
            

    @commands.is_owner()            
    @commands.group(name="errors", aliases=["error"])
    async def _errors(self, ctx):
        if not ctx.invoked_subcommand:
            async with self.bot.db.pool.acquire() as con:
                errordata = await con.fetch("SELECT * FROM errors")
                
            if not errordata:
                return await ctx.embed(title="All clear!", description="Looks like there is no errors at the moment!", colour=self.bot.good_embed_colour, reply=True)
            
            else:
                errordata = [dict(record) for record in errordata]
                
                embed = discord.Embed(title="Errors", colour=self.bot.bad_embed_colour)
                
                commanderrordict = {}
                for error in errordata:
                    commanderrordict[error["command"]] = [*commanderrordict.get(error["command"], []), str(error["id"])]
                    
                for command in commanderrordict:
                    embed.add_field(name=command, value=", ".join([f"`{error}`" for error in commanderrordict[command]]))
                    
                await ctx.reply(embed=embed, mention_author=False)
    
    @commands.is_owner()        
    @_errors.command(name="view")
    async def _errors_view(self, ctx, errorid: int):
        async with self.bot.db.pool.acquire() as con:
            data = await con.fetch("SELECT * FROM errors WHERE id=$1", errorid)
            
        if not data:
            return await ctx.error("No error with that id!")
        else:
            await ctx.embed(title=f"Error number {errorid}", description=f"```\n{data[0]['shorterror'] or 'No short description'}```\n```py\n{data[0]['traceback'] or 'No traceback availiable'}```", colour=self.bot.bad_embed_colour, footertext=f"Invoked by {str(self.bot.get_user(data[0]['user_id']) or self.bot.fetch_user(data[0]['user_id']))}", footerurl=(self.bot.get_user(data[0]['user_id']) or self.bot.fetch_user(data[0]['user_id'])).avatar.url)

    @commands.is_owner()
    @_errors.command(name="fix")
    async def _errors_fix(self, ctx, errorid: int):
        async with self.bot.db.pool.acquire() as con:
            await con.execute("DELETE FROM errors WHERE id=$1", errorid)
            
        await ctx.message.add_reaction("\U0001f44d")

def setup(bot):
    bot.add_cog(Errors(bot))
