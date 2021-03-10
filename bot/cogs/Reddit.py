import discord
from discord.ext import commands
import aiohttp
import random
import textwrap


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reddit")
    async def _reddit(self, ctx, subreddit):
        with ctx.channel.typing():
            try:
                if subreddit.startswith("r/"):
                    subreddit = subreddit[2:]

                async with aiohttp.ClientSession() as con:
                    async with con.get(f"https://www.reddit.com/r/{subreddit}/.json") as r:
                        data = await r.json()

                if data["data"]["children"]:
                    if ctx.channel.is_nsfw():
                        for _ in range(1, 30):
                            post = random.choice(data["data"]["children"])
                            if post["data"]["domain"] == "i.redd.it" and not post["data"]["stickied"]:
                                break
                            else:
                                post = None

                    else:
                        for _ in range(1, 30):
                            post = random.choice(data["data"]["children"])
                            if post["data"]["domain"] in ["i.redd.it"] and not post["data"]["stickied"] and not post["data"]["over_18"]:
                                break
                            else:
                                post = None

                    if post:
                        embed = discord.Embed(title=textwrap.fill(
                            post["data"]["title"], width=35), url=f"https://www.reddit.com{post['data']['permalink']}", colour=discord.Colour.teal())
                        embed.set_image(url=post["data"]["url"])
                        embed.add_field(
                            name="Upvotes", value=f"```py\n{int(post['data']['ups']) - int(post['data']['downs'])}```", inline=True)
                        embed.set_footer(
                            text=f"Uploaded by u/{post['data']['author']}", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Error!", description=f"```diff\n- Failed getting a post from {subreddit}! (This may be because the post was a video, which is unsupported)```", colour=discord.Colour.red()).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching {subreddit}!```", colour=discord.Colour.red()).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

            except Exception as e:
                if isinstance(e, KeyError):
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching {subreddit}!```", colour=discord.Colour.red()).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- There was an error, please try again later```", colour=discord.Colour.red())
                    await ctx.send(embed=embed)

    @commands.command(name="cat", aliases=["cats"])
    async def _cat(self, ctx):
        await self._reddit(ctx, "cutecats")
        
    @commands.command(name="dog", aliases=["dogs", "doggo", "doggos"])
    async def _dog(self, ctx):
        await self._reddit(ctx, "doggos")
        
    @commands.command(name="meme", aliases=["memes"])
    async def _meme(self, ctx):
        await self._reddit(ctx, "memes")
    
def setup(bot):
    bot.add_cog(Reddit(bot))
