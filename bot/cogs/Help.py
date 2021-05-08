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

import discord
from discord.ext import commands

import datetime
import discord
from discord.ext import commands
from discord.ext.commands.core import Group
import textwrap
import humanize
from .backend.paginator.paginator import paginator, input


class helpcommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        ctx = self.context
        thehelp = await self.get_bot_help(mapping, ctx)

        if isinstance(thehelp, list):
            embeds = [*thehelp]
        else:
            embeds = thehelp
        
        for cog in mapping:
            if cog and mapping[cog] and await self.include_cog(cog):
                coghelp = await self.get_cog_help(cog, ctx)
                
                for page in coghelp:
                    embeds.append(page)

        await self.send_the_help(ctx, embeds)

    async def send_cog_help(self, cog):
        ctx = self.context
        thehelp = await self.get_cog_help(cog, ctx)

        if isinstance(thehelp, list):
            embeds = [*thehelp]
        else:
            embeds = thehelp
            
        await self.send_the_help(ctx, embeds)

    async def send_group_help(self, group):
        ctx = self.context
        thehelp = await self.get_group_help(group, ctx)
        if isinstance(thehelp, list):
            if len(thehelp) == 1:
                embeds = thehelp[-1]
            else:
                embeds = [*thehelp]
        else:
            embeds = thehelp

        await self.send_the_help(ctx, embeds)

    async def send_command_help(self, command):
        ctx = self.context

        await self.send_the_help(ctx, await self.get_command_help(command))

    async def get_bot_help(self, mapping, ctx):
        pages = {}

        for cog in mapping:
            if cog and await self.include_cog(cog):
                pages[str(cog.qualified_name.capitalize() if cog.qualified_name else "No name")] = str(
                    cog.description.capitalize() if cog.description else "No description")

        pages = {b: textwrap.shorten(
            pages[b], width=51, break_long_words=True, placeholder="...") for b in sorted(pages)}
        
        keys = [list(pages)[n:n+6] for n in range(0, len(list(pages)), 6)]
        listofsmalldescriptions = []
        for i in keys:
            temp = {}  
            for key in i:
                temp[key] = pages[key]
            listofsmalldescriptions.append(temp)
        
        for index, page in enumerate(listofsmalldescriptions):
            listofsmalldescriptions[index] = (
                "\n".join([f"{i}: {page[i]}" for i in page])).replace("`", "\u200b`\u200b")
        
        result = []

        for item, i in enumerate(listofsmalldescriptions):
            if item == 0:
                result.append(input(discord.Embed(title="Help", url="https://bit.ly/Elli0t",
                                            description=f"{ctx.bot.description}\n```yaml\n{i}```", colour=self.context.bot.neutral_embed_colour).set_footer(text=f"Type {self.context.clean_prefix}help <category> for more help on a category", icon_url=ctx.author.avatar.url), None))
            else:
                result.append(input(discord.Embed(title="Help", url="https://bit.ly/Elli0t",
                                            description=f"```yaml\n{i}```", colour=self.context.bot.neutral_embed_colour).set_footer(text=f"Type {self.context.clean_prefix}help <category> for more help on a category", icon_url=ctx.author.avatar.url), None))

        return result

    async def get_cog_help(self, cog, ctx):
        pages = {}
        for command in cog.get_commands():
            pages[str(command.name.capitalize() if command.name else "No name")] = str(
                command.help.capitalize() if command.help else "No description")
        pages = {b: textwrap.shorten(
            pages[b], width=51, break_long_words=True, placeholder="...") for b in sorted(pages)}
        
        keys = [list(pages)[n:n+6] for n in range(0, len(list(pages)), 6)]
        listofsmalldescriptions = []
        for i in keys:
            temp = {}  
            for key in i:
                temp[key] = pages[key]
            listofsmalldescriptions.append(temp)

        for index, page in enumerate(listofsmalldescriptions):
            listofsmalldescriptions[index] = ("\n".join(
                [f"{i}: {page[i]}" for i in page])).replace("`", "\u200b`\u200b")

        result = []

        for item, i in enumerate(listofsmalldescriptions):
            if item == 0:
                result.append(input(discord.Embed(title=cog.qualified_name.capitalize() if cog.qualified_name else "Help", url="https://bit.ly/Elli0t",
                                            description=f"{cog.description.capitalize() if cog.description else 'No description'}\n```yaml\n{i}```", colour=self.context.bot.neutral_embed_colour).set_footer(text=f"Type {self.context.clean_prefix}help <command> for more help on a command", icon_url=ctx.author.avatar.url), None))
            else:
                result.append(input(discord.Embed(title=cog.qualified_name.capitalize() if cog.qualified_name else "Help", url="https://bit.ly/Elli0t",
                                            description=f"```yaml\n{i}```", colour=self.context.bot.neutral_embed_colour).set_footer(text=f"Type {self.context.clean_prefix}help <command> for more help on a command", icon_url=ctx.author.avatar.url), None))
        return result

    async def get_group_help(self, group, ctx):
        if await self.include_cog(group.cog):
            pages = {}
            for command in group.commands:
                pages[str(command.name.capitalize() if command.name else "No name")] = str(
                    command.help.capitalize() if command.help else "No description")
            pages = {b: textwrap.shorten(
                pages[b], width=51, break_long_words=True, placeholder="...") for b in sorted(pages)}
            
            keys = [list(pages)[n:n+6] for n in range(0, len(list(pages)), 6)]
            listofsmalldescriptions = []
            for i in keys:
                temp = {}  
                for key in i:
                    temp[key] = pages[key]
                listofsmalldescriptions.append(temp)
            
            for index, page in enumerate(listofsmalldescriptions):
                listofsmalldescriptions[index] = ("\n".join([f"{i}: {page[i]}" for i in page])).replace("`", "\u200b`\u200b")

            result = []

            for item, i in enumerate(listofsmalldescriptions):
                if item == 0:
                    result.append(input(discord.Embed(title=group.name.capitalize() if group.name else "Help", url="https://bit.ly/Elli0t",
                                                description=f"```\n{self.get_command_signature(group)}```\n{group.help.capitalize() if group.help else 'No help'}\n```yaml\n{i}```", colour=self.context.bot.neutral_embed_colour).set_footer(text=f"Type {self.context.clean_prefix}help <command> for more help on a command", icon_url=ctx.author.avatar.url), None))
                else:
                    result.append(input(discord.Embed(title=group.name.capitalize() if group.name else "Help", url="https://bit.ly/Elli0t",
                                                description=f"```yaml\n{i}```", colour=self.context.bot.neutral_embed_colour).set_footer(text=f"Type {self.context.clean_prefix}help <command> for more help on a command", icon_url=ctx.author.avatar.url), None))
            return result
        else:
            return await self.command_not_found(group.name)

    async def get_command_help(self, command):
        if await self.include_cog(command.cog):
            usagestring = self.get_command_signature(command)
            embed = discord.Embed(title=command.name.capitalize() if command.name else "Help", url="http://bit.ly/Elli0t",
                                    description=f"```\n{usagestring}```\n{command.help or 'No help provided'}", colour=self.context.bot.neutral_embed_colour)
            cooldown = command._buckets._cooldown
            if cooldown:
                embed.add_field(
                    name="Cooldown", value=f"```yaml\n{cooldown.rate} times per {humanize.precisedelta(datetime.timedelta(seconds=cooldown.per))}```" if cooldown else '```yaml\nNone```')
            embed.add_field(
                name="Runnable?", value="```yaml\nYes```" if command in await self.filter_commands([command]) else '```yaml\nNo```')
            embed.add_field(
                name="Category", value=f"```yaml\n{command.cog.__class__.__name__}```"
            )
            return embed
        else:
            return await self.command_not_found(command.name)

    async def include_cog(self, cog):
        return (cog.qualified_name not in ["Owner", "Dev", "Jishaku", "Statcord"]) if self.context.author.id != self.context.bot.owner_id else True

    async def command_not_found(self, string):
        return discord.Embed(
            title="Error!",
            description=f"Couldn't find the command `{string}`!",
            colour=self.context.bot.neutral_embed_colour,
        )

    async def subcommand_not_found(self, command, string):
        if isinstance(command, Group) and len(command.all_commands) > 0:
            return discord.Embed(
                title="Error!",
                description=f"The command `{command.qualified_name}` has no subcommand `{string}`!",
                colour=self.context.bot.neutral_embed_colour,
            )

        else:
            return discord.Embed(
                title="Error!",
                description=f"The command `{command.qualified_name}` has no subcommands!",
                colour=self.context.bot.neutral_embed_colour,
            )

    def split(self, a, sep, pos):
        if a.count(sep) == 1:
            return a.split(sep)[0]
        if (newpos := a.count(sep)) < pos:
            return [sep.join(a.split(sep, newpos + 1)[:newpos + 1]), a.split(sep, newpos + 1)[newpos + 1:][0]]
        return [sep.join(a.split(sep, pos)[:pos]), a.split(sep, pos)[pos:][0]]

    async def send_error_message(self, error):
        destination = self.get_destination()
        if isinstance(error, discord.Embed):
            await destination.send(embed=error)
        else:
            await destination.send(error)

    async def send_the_help(self, ctx, thehelp):
        if isinstance(thehelp, list):
            if len(thehelp) == 0:
                return await ctx.reply(embed=await self.command_not_found(ctx.message.content.split("help ")[-1]))
            pages = paginator(ctx, remove_reactions=True)
            pages.add_reaction("\U000023ea", "first")
            pages.add_reaction("\U000025c0", "back")
            pages.add_reaction("\U0001f5d1", "delete")
            pages.add_reaction("\U000025b6", "next")
            pages.add_reaction("\U000023e9", "last")
            await pages.send(thehelp)

        elif isinstance(thehelp, discord.Embed):
            await ctx.reply(embed=thehelp)

        else:
            if isinstance(thehelp, input):
                await ctx.reply(embed=thehelp.content, file=thehelp.picture)
            else:
                await ctx.reply(thehelp)


class Help(commands.Cog):
    '''
    The help menu
    '''
    def __init__(self, bot):
        self.bot = bot
        self.bot._original_help_command = bot.help_command
        bot.help_command = helpcommand(command_attrs=dict(aliases=["h", "?"]))  

        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.bot._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
