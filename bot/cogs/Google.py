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

import aiohttp
import discord
from async_cse import Search
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
from .backend.google.scraper import get_results
from .backend.paginator.paginator import paginator, input

class Google(commands.Cog):
    def __init__(self, bot):
        '''
        Commands related to google
        '''
        self.bot = bot    
    
    @commands.cooldown(1, 5, BucketType.member)
    @commands.command(name="google", aliases=["g"])
    async def _google(self, ctx, *, query):
        with ctx.typing():
            results = await get_results(query, ctx)

        if not any(results):
            embed = discord.Embed(
                title="Error!", description=f"```diff\n- Couldn't find anything matching {query}!```", colour=self.bot.bad_embed_colour)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            websitelist = []
            if results.websites:
                websites = [results.websites[n:n+3]
                            for n in range(0, len(results.websites), 3)]
                for page in websites:
                    websitestring = "".join(
                        f"[**{discord.utils.escape_markdown(site.title)}**]({site.link})\n{discord.utils.escape_markdown(str(site.description))}\n\n"
                        for site in page
                    )

                    websitelist.append(websitestring)

            embed = None
            picture = None
            if results.calculator:
                calculator_string = ""
                if results.calculator.input:
                    calculator_string += f"**{results.calculator.input}**\n"
                if results.calculator.output:
                    calculator_string += f"{results.calculator.output}"
                embed = discord.Embed(
                    title=f"Search results for {query}", description=calculator_string, colour=self.bot.neutral_embed_colour)

            elif results.knowledge:
                knowledge_string = ""
                if results.knowledge.title:
                    knowledge_string += f"**{results.knowledge.title}**\n"
                if results.knowledge.subtitle:
                    knowledge_string += f"{results.knowledge.subtitle}\n"
                if results.knowledge.description["description"]:
                    knowledge_string += f"\n{results.knowledge.description['description']}\n"
                    if results.knowledge.description["wiki"]["text"] and results.knowledge.description["wiki"]["link"]:
                        knowledge_string = knowledge_string.strip('\n')
                        knowledge_string = (
                            f"{knowledge_string} [**{results.knowledge.description['wiki']['text']}**]({results.knowledge.description['wiki']['link']})\n")
                picture = None
                if results.knowledge.image:
                    picture = discord.File(
                        results.knowledge.image, f"{query.replace(' ', '_')}.png")
                embed = discord.Embed(
                    title=f"Search results for {query}", description=knowledge_string.strip('\n'), colour=self.bot.neutral_embed_colour)

                if picture:
                    embed.set_thumbnail(url=f"attachment://{picture.filename}")

            elif results.location:
                location_string = ""
                if results.location.top:
                    location_string += f"**{results.location.top}**\n"
                if results.location.bottom:
                    location_string += f"{results.location.bottom}\n"
                picture = None
                if results.location.image:
                    picture = discord.File(
                        results.location.image, f"{query.replace(' ', '_')}.png")

                embed = discord.Embed(title=f"Search results for {query}", description=location_string.strip(
                    '\n'), colour=self.bot.neutral_embed_colour)
                if picture:
                    embed.set_image(url=f"attachment://{picture.filename}")

            elif results.featured_snippet:
                snippet_string = ""
                if results.featured_snippet.title:
                    snippet_string += f"**{results.featured_snippet.title}**\n"
                if results.featured_snippet.description:
                    snippet_string += f"{results.featured_snippet.description}\n"
                if results.featured_snippet.link["name"] and results.featured_snippet.link["href"]:
                    snippet_string += f"[{results.featured_snippet.link['name']}]({results.featured_snippet.link['href']})\n"

                embed = discord.Embed(title=f"Search results for {query}", description=snippet_string.strip(
                    '\n'), colour=self.bot.neutral_embed_colour)

            if embed:
                results = []
                if websitelist:
                    page = websitelist[0].strip("\n")
                    embed.description = f"{embed.description}\n\n{page}"
                    results.append(input(embed, picture))
                    if len(websitelist) > 1:
                        for page in websitelist[1:]:
                            embed = discord.Embed(description=page.strip(
                                "\n"), colour=self.bot.neutral_embed_colour)
                            if picture:
                                embed.set_thumbnail(
                                    url=f"attachment://{picture.filename}")
                            results.append(input(embed, picture))
                        pages = paginator(ctx, remove_reactions=True)
                        pages.add_reaction("\U000023ea", "first")
                        pages.add_reaction("\U000025c0", "back")
                        pages.add_reaction("\U0001f5d1", "delete")
                        pages.add_reaction("\U000025b6", "next")
                        pages.add_reaction("\U000023e9", "last")
                        await pages.send(results)
                    else:
                        await ctx.reply(embed=embed, mention_author=False)
            else:
                if websitelist:
                    results = []
                    embed = discord.Embed(
                        title=f"Search results for {query}", description="", colour=self.bot.neutral_embed_colour)
                    page = websitelist[0].strip("\n")
                    embed.description = f"{embed.description}\n\n{page}"
                    results.append(input(embed, picture))
                    if len(websitelist) > 1:
                        for page in websitelist[1:]:
                            embed = discord.Embed(description=page.strip(
                                "\n"), colour=self.bot.neutral_embed_colour)
                            if picture:
                                embed.set_thumbnail(
                                    url=f"attachment://{picture.filename}")
                            results.append(input(embed, picture))
                        pages = paginator(ctx, remove_reactions=True)
                        pages.add_reaction("\U000023ea", "first")
                        pages.add_reaction("\U000025c0", "back")
                        pages.add_reaction("\U0001f5d1", "delete")
                        pages.add_reaction("\U000025b6", "next")
                        pages.add_reaction("\U000023e9", "last")
                        await pages.send(results)
                    else:
                        await ctx.reply(embed=embed, mention_author=False)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching {query}!```", colour=self.bot.bad_embed_colour)
                    await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(Google(bot))
