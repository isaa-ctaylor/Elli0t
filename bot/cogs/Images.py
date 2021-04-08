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

import os

from asyncdagpi import Client as dpClient, ImageFeatures
from aiozaneapi import Client as zClient
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
from typing import Optional, Union, Literal
load_dotenv()

class Images(commands.Cog):
    '''
    Image manipulation
    '''

    def __init__(self, bot):
        self.bot = bot
        self.dagpiclient = dpClient(os.getenv("ASYNCDAGPI"))
        

    @commands.Cog.listener(name="cog_command_error")
    async def _cog_error(self, ctx, error):
        if isinstance(error, aiohttp.client_exceptions.ContentTypeError):
            embed = discord.Embed(title="Error", description="There was an error, please try again later", colour=self.bot.bad_embed_colour)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            raise error
    
    @commands.command(name="avatar")
    async def _avatar(self, ctx, *, member: discord.Member = None):
        '''
        Get the avatar of the given member
        '''
        member = member or ctx.author
        
        embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s avatar", colour=member.colour)
        embed.set_image(url=member.avatar_url_as(format=None, static_format="png"))
        
        await ctx.reply(embed=embed, mention_author=False)
        
    
    async def process_image(self, ctx, member, proccesstype):
        url = str(member.avatar_url_as(
            format="png", static_format="png", size=1024))
        img = await self.dagpiclient.image_process(proccesstype, url)
        file = discord.File(fp=img.image, filename=f"image.{img.format}")
        return file
    
    @commands.command(name="pixel", aliases=["pixelate"])
    async def _pixelate(self, ctx, *, member: discord.Member):
        '''
        Pixelate the given member
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.pixel()))

    @commands.command(name="colours", aliases=["colors"])
    async def _colours(self, ctx, *, member: discord.Member):
        '''
        Analyse the colours of the given member
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.colors()))

    @commands.command(name="wanted", aliases=["want"])
    async def _wanted(self, ctx, *, member: discord.Member):
        '''
        Just like in the wild west
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.wanted()))

    @commands.command(name="triggered", aliases=["trigger"])
    async def _triggered(self, ctx, *, member: discord.Member):
        '''
        REEEE
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.triggered()))

    @commands.command(name="america")
    async def _america(self, ctx, *, member: discord.Member):
        '''
        Good ol' america
        '''
        await ctx.send("Please wait, this may take some time")
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.america()))

    @commands.command(name="wasted")
    async def _wasted(self, ctx, *, member: discord.Member):
        '''
        GTA but in discord
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.wasted()))

    @commands.command(name="invert")
    async def _invert(self, ctx, *, member: discord.Member):
        '''
        Invert the picture
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.invert()))

    @commands.command(name="triangle")
    async def _triangle(self, ctx, *, member: discord.Member):
        '''
        Triangles
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.triangle()))

    @commands.command(name="hog")
    async def _hog(self, ctx, *, member: discord.Member):
        '''
        Not really sure about this one either
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.hog()))

    @commands.command(name="blur")
    async def _blur(self, ctx, *, member: discord.Member):
        '''
        Forgotten your glasses?
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.blur()))

    @commands.command(name="rgb")
    async def _rgb(self, ctx, *, member: discord.Member):
        '''
        Analyse the rgb
        '''
        await ctx.send("Please wait, this may take some time")
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.rgb()))

    @commands.command(name="obama")
    async def _obama(self, ctx, *, member: discord.Member):
        '''
        The man the myth the legend
        '''
        await ctx.send("Please wait, this may take some time")
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.obama()))
            
    @commands.command(name="jail")
    async def _jail(self, ctx, *, member: discord.Member):
        '''
        You have been jailed
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.jail()))
            
    @commands.command(name="gay")
    async def _gay(self, ctx, *, member: discord.Member):
        '''
        Pride
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.gay()))
            
    @commands.command(name="deepfry")
    async def _deepfry(self, ctx, *, member: discord.Member):
        '''
        Like chips
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.deepfry()))

    @commands.command(name="ascii")
    async def _ascii(self, ctx, *, member: discord.Member):
        '''
        Your image, but ascii
        '''
        with ctx.channel.typing():
            await ctx.send(file=await self.process_image(ctx, member, ImageFeatures.ascii()))
    
def setup(bot):
    bot.add_cog(Images(bot))