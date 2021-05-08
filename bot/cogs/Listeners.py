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
from collections import Counter

import humanize
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
            
    @commands.Cog.listener(name="on_message_edit")
    async def _reinvoke_commands(self, before, after):
        if after.content != before.content:
            await self.bot.process_commands(after)
            
    @commands.Cog.listener(name="on_message")
    async def _send_prefix(self, message):
        if message.content in [str(self.bot.user.mention), "<@!778637164388810762>", str(ctx.guild.me.mention)]:
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
    async def _log_guild_join(self, guild: discord.Guild):
        embed = discord.Embed(title="New guild!", colour=self.bot.neutral_embed_colour)
        embed.add_field(name="Guild name", value=f"```\n{guild.name}```", inline=True)
        embed.add_field(name="Guild owner", value=f"```\n{guild.owner} - ({guild.owner.id})```", inline=True)
        embed.add_field(name="Guild members", value=f"```\n{guild.member_count}```", inline=True)
        embed.add_field(name="Guild region", value=f"```\n{str(guild.region).capitalize()}```", inline=True)
        embed.add_field(name="Guild created", value=f"```\n{humanize.naturaldate(guild.created_at)}```", inline=True)
        embed.set_thumbnail(url=guild.icon.url)
        await self.bot.get_channel(839200251347730473).send(embed=embed)

    @commands.Cog.listener(name="on_guild_leave")
    async def _log_guild_join(self, guild: discord.Guild):
        try:
            embed = discord.Embed(title="Got removed from a guild!", description=f"Got removed from `{guild.name}` losing `{guild.member_count}` members!")
            await self.bot.get_channel(839200251347730473).send(embed=embed)
        except Exception as e:
            self.logger.error(e)
            await self.bot.get_channel(839200251347730473).send(e)

    async def _check_not_blacklisted(self, ctx):
        if str(ctx.author.id) not in list(self.bot.blacklist):
            return True
    
def setup(bot):
    bot.add_cog(Listeners(bot))
