import discord
from pexels_api import API
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

load_dotenv()

pexels = API(os.getenv("PEXELS_ID"))

class Photos(commands.Cog):
    '''
    Beautiful photos using the free pexels API: https://www.pexels.com/api/
    '''
    def __init__(self, bot):
        self.bot=bot


    @commands.command(name = "picture", aliases = ["photo"])
    async def _picture(self, ctx, *, query):
        search = pexels.search(query, page = 1, results_per_page = 80)
        photos = pexels.get_entries()
        
        picture_embed = discord.Embed(title = "Here ya go!", colour = discord.Colour.random())
        num = random.randint(0, 79)
        try:
            picture_embed.set_image(url = photos[num].original)
            picture_embed.add_field(name = "Credits", value = f"Photo by [{photos[num].photographer}]({photos[num].photographer_url}) on [Pexels](https://www.pexels.com/)")
        except IndexError:
            try:
                picture_embed.set_image(url = photos[0].original)
                picture_embed.add_field(name = "Credits", value = f"Photo by [{photos[0].photographer}]({photos[0].photographer_url}) on [Pexels](https://www.pexels.com/)")
                await ctx.send(embed = picture_embed)
            except IndexError:
                error_embed = discord.Embed(title = "Sorry!", description = "I couldn't find the picture you were looking for!", colour = discord.Colour.red())
                await ctx.send(embed = error_embed)
        else:
            await ctx.send(embed = picture_embed)
    
    
    
def setup(bot):
    bot.add_cog(Photos(bot))