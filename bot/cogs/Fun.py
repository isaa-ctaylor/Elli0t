import discord
import random
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        
def setup(bot):
    bot.add_cog(Fun(bot))
