import discord
from discord.ext import commands
from async_cse import Search
import aiohttp


class Internet(commands.Cog):
    def __init__(self, bot):
        '''
        Commands related to the internet
        '''
        self.bot = bot
        self.google = Search(["AIzaSyAlfCEUbpQi8Vpb22MdNcdTUuWu-DQrB8U",
                              "AIzaSyAAW_OtBeO49Q6NG-WwF-_y9IQUtH0ZSKc",
                              "AIzaSyBZCUM0JETBwSYxg6VLKQt1f_ZduVthxeY",
                              "AIzaSyCK2jkvgHPec7yn6y9p7R55J1o4tfMr4cQ",
                              "AIzaSyBfq0ExH-QSqBTZTLjiCIyylQVP_xJ0Lec"])
    
    @commands.command(name="google", aliases=["g"])
    async def _google(self, ctx, *, query):
        '''
        Search google
        '''
        with ctx.channel.typing():
            try:
                result = await self.google.search(query)
                urlformat = query.replace(" ", "+")
                embed = discord.Embed(title=f"Search results for {query}:", url=f"https://www.google.com/search?safe=active&q={urlformat}", colour=discord.Colour.green())
                for entry in result[:3]:
                    embed.add_field(name=entry.title, value=f"{entry.url}\n{entry.description}", inline=False)
                
                embed.set_thumbnail(url=result[0].image_url or None)
                
                await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="Error!", description=f"```diff\n- {e}```", colour=discord.Colour.red())
                await ctx.send(embed=embed)
                
    @commands.command(name="lengthen")
    async def _lengthen(self, ctx, *, url):
        try:
            with ctx.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        url = str(response.url)
                        embed = discord.Embed(title="Success!", url=url, description=f"`{url}`", colour=discord.Colour.green())
                        await ctx.send(embed=embed)
        except aiohttp.InvalidURL:
            embed = discord.Embed(title="Error!", description=f"```diff\n- Invalid URL: {url}```", colour=discord.Colour.red())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Internet(bot))
