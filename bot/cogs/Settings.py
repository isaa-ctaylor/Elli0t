import discord
from discord.ext import commands
import json


class Settings(commands.Cog):
    '''Settings for your guild'''
    def __init__(self, bot):
        self.bot=bot


    @commands.group(name = "settings")
    async def _settings(self, ctx):
        if not ctx.invoked_subcommand:
            settings_embed = discord.Embed(title = "Settings 🔧", description = "Use the command settings with any of the options below to configure them", colour = discord.Color.green())
            settings_embed.add_field(name = "prefix", value = "Change the prefix for your server!", inline = True)
            settings_embed.add_field(name = "tickets", value = "Configure tickets for your server!", inline = True)
            settings_embed.add_field(name = "chat", value = "Configure the chat filter", inline = True)



    @_settings.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        '''Changes the prefix for your server, the prefix can be absolutely anything you want!

        Usage
        -----
        prefix <prefix>

        Parameters
        ----------
        ctx: discord.Context
            The invocation context
        prefix: str
            The prefix to change to
        '''
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        try:
            await ctx.guild.get_member(self.bot.user.id).edit(nick = f"[{prefix}] Elli0t", reason = "Change nick to encompass prefix")
        except discord.Forbidden:
            pass
        
        if prefix == "`":
            await ctx.send(f'Prefix changed to: {prefix}')
        else:
            await ctx.send(f'Prefix changed to: `{prefix}`')


def setup(bot):
    bot.add_cog(Settings(bot))