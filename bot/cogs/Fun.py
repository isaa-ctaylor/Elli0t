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
import random
from discord.ext import commands
import xkcd_wrapper
import aiohttp
from sr_api import Client
from inflect import engine

class Fun(commands.Cog):
    '''
    Fun commands for when you are bored :D
    '''
    def __init__(self, bot):
        self.bot = bot
        self.xkcd = xkcd_wrapper.AsyncClient()
        self.srapi = Client()
        self.inflect = engine()

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question):
        '''
        Ask the wise magic 8ball
        '''
        await ctx.send(random.choice(["As I see it, yes.",
                                      "Ask again later.",
                                      "Better not tell you now.",
                                      "Cannot predict now.",
                                      "Concentrate and ask again.",
                                      "Don’t count on it.",
                                      "It is certain.",
                                      "It is decidedly so.",
                                      "Most likely.",
                                      "My reply is no.",
                                      "My sources say no.",
                                      "Outlook not so good.",
                                      "Outlook good.",
                                      "Reply hazy, try again.",
                                      "Signs point to yes.",
                                      "Very doubtful.",
                                      "Without a doubt.",
                                      "Yes.",
                                      "Yes – definitely.",
                                      "You may rely on it."]))

    @commands.command(name="lick", aliases=["mlem"])
    async def _lick(self, ctx, person: discord.Member):
        '''
        Mlem
        '''
        if person == ctx.author:
            return await ctx.send("You can't lick yourself!")
        
        if person == self.bot.user:
            return await ctx.send("I don't like being licked!")

        tastesLike = [
            "bacon",
            "tortilla chips",
            "chezborger",
            "ketchup on pasta",
            "bubblegum",
            "chicken",
            "honey",
            "a creeper",
            "corn",
            "butts",
            "a jolly rancher",
            "cheese",
            "pickles",
            "lemons",
            "cucumbers"
        ]
        
        await ctx.send(f"{ctx.author.mention} licked {person.mention}! They taste like {random.choice(tastesLike)}!")
        
    @commands.command(name="xkcd")
    async def _xkcd(self, ctx, number: int=None):
        '''
        Get an xkcd comic
        '''
        try:
            with ctx.typing():
                if number:
                    try:
                        comic = await self.xkcd.get(number)
                    except TypeError:
                        embed = discord.Embed(title="Error!", description=f"Couldn't find comic {number}", colour=self.bot.bad_embed_colour)
                else:
                    comic = await self.xkcd.get_random()
                
                if comic:
                    embed = discord.Embed(title=comic.title, description=f"[Comic number {comic.id}]({comic.comic_url})\n{comic.description}", colour=self.bot.neutral_embed_colour)
                    embed.set_image(url = comic.image_url)
        
        except Exception as e:
            await ctx.send(type(e))
            embed = discord.Embed(title="Error!", description="There was an error, please try again soon", colour=self.bot.bad_embed_colour)        
        await ctx.send(embed = embed)
    
    @commands.group(name="fact")
    async def _fact(self, ctx):
        if not ctx.invoked_subcommand:
            with ctx.typing():
                categories = [
                    "cat",
                    "dog",
                    "koala",
                    "fox",
                    "bird",
                    "elephant",
                    "panda",
                    "racoon",
                    "kangaroo",
                    "giraffe",
                    "whale"
                ]
                animal = random.choice(categories)
                fact = await self.srapi.get_fact(animal)
                embed = discord.Embed(title=f"A fun fact about {self.inflect.plural(animal)}", description=fact, colour=self.bot.neutral_embed_colour)
                await ctx.reply(embed=embed, mention_author=False)
    
    @_fact.command(name="cat")
    async def _fact_cat(self, ctx):
        animal = "cat"
        fact = await self.srapi.get_fact(animal)
        embed = discord.Embed(
            title=f"A fun fact about {self.inflect.plural(animal)}", description=fact, colour=self.bot.neutral_embed_colour)
        await ctx.reply(embed=embed, mention_author=False)
    
    @_fact.command(name="dog")
    async def _fact_dog(self, ctx):
        animal = "dog"
        fact = await self.srapi.get_fact(animal)
        embed = discord.Embed(title=f"A fun fact about {self.inflect.plural(animal)}", description=fact, colour=self.bot.neutral_embed_colour)
        await ctx.reply(embed=embed, mention_author=False)
    
    @_fact.command(name="koala")
    async def _fact_koala(self, ctx):
        animal = "koala"
        fact = await self.srapi.get_fact(animal)
        embed = discord.Embed(title=f"A fun fact about {self.inflect.plural(animal)}", description=fact, colour=self.bot.neutral_embed_colour)
        await ctx.reply(embed=embed, mention_author=False)
        
    @_fact.command(name="fox")
    async def _fact_fox(self, ctx):
        animal = "fox"
        fact = await self.srapi.get_fact(animal)
        embed = discord.Embed(title=f"A fun fact about {self.inflect.plural(animal)}", description=fact, colour=self.bot.neutral_embed_colour)
        await ctx.reply(embed=embed, mention_author=False)
        
    @_fact.command(name="bird")
    async def _fact_bird(self, ctx):
        animal = "bird"
        fact = await self.srapi.get_fact(animal)
        embed = discord.Embed(title=f"A fun fact about {self.inflect.plural(animal)}", description=fact, colour=self.bot.neutral_embed_colour)
        await ctx.reply(embed=embed, mention_author=False)
    
def setup(bot):
    bot.add_cog(Fun(bot))
