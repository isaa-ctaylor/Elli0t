import discord
from discord.ext import commands
import re
from typing import Optional
from .backend.paginator.paginator import paginator
import logging
logging.getLogger("discord")

class Emojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = ["<:Elite:794608720688185364>"]
        self.cache = {}

    async def updatecache(self):
        async with self.bot.db.pool.acquire() as con:
            emojis = await con.fetch("SELECT * FROM userdata")
        
        tempcache = {}
        for person in emojis:
            tempcache[int(person["user_id"])] = person["emojis"]
        
        self.cache = tempcache
    
    @commands.Cog.listener(name="on_message")
    async def _send_emojis(self, message):
        if not self.cache:
            await self.updatecache()

        if (int(message.author.id) in list(self.cache)):
            if self.cache[int(message.author.id)] == True:
                emojistosend = []
                foundemojinames = re.findall(
                    r"((?<=\.).+?(?=\.|$|\s))", str(message.content))

                if foundemojinames:
                    guildemojinames = {
                        emoji.name.lower(): emoji.name for emoji in message.guild.emojis}
                    botemojinames = {
                        emoji.name.lower(): emoji.name for emoji in self.bot.emojis}
                    for emojiname in foundemojinames:
                        found = False
                        for emoji in guildemojinames:
                            if emoji == emojiname.lower():
                                foundemoji = discord.utils.get(
                                    message.guild.emojis, name=guildemojinames[emoji])
                                found = True
                                break
                        if not found:
                            for emoji in botemojinames:
                                if emoji == emojiname.lower():
                                    foundemoji = discord.utils.get(
                                        self.bot.emojis, name=botemojinames[emoji])
                                    found = True
                                    break
                        if not found:
                            pass
                        else:
                            if foundemoji:
                                if not str(foundemoji) in self.whitelist:
                                    emojistosend.append(str(foundemoji))

                    if emojistosend:
                        if not message.reference:
                            await message.reply(" ".join(emojistosend), mention_author=False)
                        else:
                            msg = await message.channel.fetch_message(message.reference.message_id)
                            for emoji in emojistosend:
                                await msg.add_reaction(emoji)

    @commands.group(name="emojis", aliases=["emoji"], invoke_without_command=True)
    async def _emojis(self, ctx, *, search: Optional[str] = None):
        if not ctx.invoked_subcommand:
            if not search:
                embeds = []
                emojis = [self.bot.emojis[n:n+10]
                        for n in range(0, len(self.bot.emojis), 10)]
                for group in emojis:
                    emojilist = []
                    for emoji in group:
                        if not str(emoji) in self.whitelist:
                            emojilist.append(f"{emoji} `{emoji.name} | {emoji.id}`")
                    embed = discord.Embed(description="\n".join(emojilist), colour=discord.Colour.random())
                    embeds.append(embed)

                pages = paginator(ctx, remove_reactions=True)
                pages.add_reaction("\U000023ea", "first")
                pages.add_reaction("\U000025c0", "back")
                pages.add_reaction("\U0001f5d1", "delete")
                pages.add_reaction("\U000025b6", "next")
                pages.add_reaction("\U000023e9", "last")
                await pages.send(embeds)
            
    @_emojis.command(name="toggle")
    async def _emojis_toggle(self, ctx):
        async with self.bot.db.pool.acquire() as con:
            emojis = await con.fetch("SELECT emojis FROM userdata WHERE user_id = $1", int(ctx.author.id))
        
        if not len(emojis):
            async with self.bot.db.pool.acquire() as con:
                await con.execute("INSERT INTO userdata values($1, $2)", int(ctx.author.id), True)
                mode = True
        
        else:
            if len(emojis):
                async with self.bot.db.pool.acquire() as con:
                    await con.execute("INSERT INTO userdata values($1, $2) ON CONFLICT (user_id) DO UPDATE SET emojis = $2 where userdata.user_id = $1", int(ctx.author.id), not emojis[0]["emojis"])
                    mode = not emojis[0]["emojis"]
        await self.updatecache()
        embed = discord.Embed(title="Success!", description=f"User emoji response `{'on' if mode else 'off'}`", colour=discord.Colour.green()).set_footer(text=f"You can trigger the emoji any time by doing \".<emojiname>\"", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Emojis(bot))
