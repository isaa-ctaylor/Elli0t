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
from discord.ext import commands
import aiohttp
import random


class Reddit(commands.Cog):
    '''
    Reddit commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reddit")
    async def _reddit(self, ctx, subreddit):
        '''
        Get a random post from the given subreddit
        '''
        with ctx.channel.typing():
            try:
                subred = subreddit[2:] if subreddit.startswith("r/") else subreddit
                async with aiohttp.ClientSession() as con:
                    async with con.get(f"https://www.reddit.com/r/{subred}/.json") as r:
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
                        embed = discord.Embed(title=
                            post["data"]["title"], url=f"https://www.reddit.com{post['data']['permalink']}", colour=discord.Colour.teal())
                        embed.set_image(url=post["data"]["url"])
                        embed.set_footer(
                            text=f"Uploaded by u/{post['data']['author']} | {int(post['data']['ups']) - int(post['data']['downs'])} upvotes", icon_url=ctx.author.avatar.url)
                        embed.set_author(
                            name=f"r/{subred}", icon_url="https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2")
                    else:
                        embed = discord.Embed(
                            title="Error!", description=f"```diff\n- Failed getting a post from {subreddit}! (This may be because the post was a video, which is unsupported)```", colour=self.bot.bad_embed_colour).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar.url)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching {subreddit}!```", colour=self.bot.bad_embed_colour).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar.url)
                await ctx.reply(embed=embed, mention_author=False)
            except Exception as e:
                if isinstance(e, KeyError):
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching {subreddit}!```", colour=self.bot.bad_embed_colour).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar.url)
                else:
                    await ctx.reply(str(e))
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- There was an error, please try again later```", colour=self.bot.bad_embed_colour)

                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="cat", aliases=["cats"])
    async def _cat(self, ctx):
        '''
        Get a cat picture from reddit
        '''
        await self._reddit(ctx, "cutecats")
        
    @commands.command(name="dog", aliases=["dogs", "doggo", "doggos"])
    async def _dog(self, ctx):
        '''
        Get a dog picture from reddit
        '''
        await self._reddit(ctx, "doggos")
        
    @commands.command(name="meme", aliases=["memes"])
    async def _meme(self, ctx):
        '''
        Get a meme from reddit
        '''
        await self._reddit(ctx, "memes")
    
def setup(bot):
    bot.add_cog(Reddit(bot))
