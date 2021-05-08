from functools import cache
import discord
from discord.ext import commands
from jishaku.codeblocks import codeblock_converter, Codeblock
import aiohttp
from .backend.paginator.paginator import paginator, input
from discord.ext.commands import BucketType
from dotenv import load_dotenv
import os

load_dotenv()

class Coding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rtfm_cache = {}

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(name="run")
    async def _run(self, ctx, language, *, code: codeblock_converter):
        '''
        Run a peice of code in the given language
        '''
        timeout = aiohttp.ClientTimeout(total=60)
        with ctx.typing():
            if not code.content:
                return await ctx.error("Please supply some code!", reply=True)
            query = {
                "language": language,
                "source": code[1],
            }
            async with aiohttp.ClientSession(timeout=timeout) as cs:
                async with cs.post("https://emkc.org/api/v1/piston/execute", data=query) as r:
                    resp = await r.json()

        if resp.get("message", None):
            return await ctx.error(resp.get("message"))

        else:
            if resp["ran"]:
                result = resp["output"].replace("`", "`\u200b")
                width = 2000
                pages = [result[i:i + width]
                            for i in range(0, len(result), width)]

                embeds = []
                for index, item in enumerate(pages):
                    if index == 0:
                        embed = discord.Embed(
                            title=f"Ran in {resp['language']}", description=f"```{code.language}\n{item}```", colour=self.bot.good_embed_colour)
                    else:
                        embed = discord.Embed(
                            description=f"```{code.language}\n{item}```", colour=self.bot.good_embed_colour)
                    embeds.append(input(embed, None))
                embedpaginator = paginator(
                    ctx, remove_reactions=True, footer=True)
                embedpaginator.add_reaction("\U000023ea", "first")
                embedpaginator.add_reaction("\U000025c0", "back")
                embedpaginator.add_reaction("\U0001f5d1", "delete")
                embedpaginator.add_reaction("\U000025b6", "next")
                embedpaginator.add_reaction("\U000023e9", "last")
                await embedpaginator.send(embeds)
            else:
                await ctx.reply(str(resp))
    

def setup(bot):
    bot.add_cog(Coding(bot))
