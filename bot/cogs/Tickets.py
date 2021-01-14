import discord
import asyncio
import random
import json
from discord.ext import commands
from cogs.global_functions import get_prefix


class Tickets(commands.Cog):
    '''An easy module for ticketing!'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticketsetup(self, ctx):
        '''A quick and easy setup for ticketing

        Usage
        -----
        ticketsetup <category name>

        Parameters
        ----------
        category_name: str
            The name of the ticket category, defaults to "Tickets"
        '''

        embed = discord.Embed(title = "Make ticket channel", description = f"Make a category and copy the id, need help with finding the id? Run the command `{get_prefix(ctx.guild.id)}devhelp`", colour = random.randint(0x000000, 0xFFFFFF))
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/735762976677691462/788796891142815754/Copy_ID.png")
        embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)


    @ticketsetup.error
    async def ticketsetup_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Please enter a category name!")

def setup(bot):
  bot.add_cog(Tickets(bot))