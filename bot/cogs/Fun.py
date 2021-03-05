import discord
import random
from discord.ext import commands
import xkcd_wrapper
import aiohttp


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xkcd = xkcd_wrapper.AsyncClient()

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
        try:
            with ctx.typing():
                if number:
                    try:
                        comic = await self.xkcd.get(number)
                    except TypeError:
                        embed = discord.Embed(title="Error!", description=f"Couldn't find comic {number}", colour=discord.Colour.red())
                else:
                    comic = await self.xkcd.get_random()
                
                if comic:
                    embed = discord.Embed(title=comic.title, description=f"[Comic number {comic.id}]({comic.comic_url})\n{comic.description}", colour=discord.Colour.random())
                    embed.set_image(url = comic.image_url)
        
        except:
            embed = discord.Embed(title="Error!", description="There was an error, please try again soon", colour=discord.Colour.red())        
        await ctx.send(embed = embed)
        
def setup(bot):
    bot.add_cog(Fun(bot))
