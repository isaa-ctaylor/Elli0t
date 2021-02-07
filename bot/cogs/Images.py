import os

from asyncdagpi import Client, ImageFeatures
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

load_dotenv()


class Images(commands.Cog):
    '''
    Image manipulation using dagpi: https://dagpi.xyz/
    '''

    def __init__(self, bot):
        self.bot = bot
        self.dagpiclient = Client(os.getenv("ASYNCDAGPI"))

    @commands.Cog.listener(name="cog_command_error")
    async def _cog_error(self, ctx, error):
        if isinstance(error, aiohttp.client_exceptions.ContentTypeError):
            embed = discord.Embed(title="Error", description="There was an error, please try again later", colour=discord.Colour.red())
            await ctx.send(embed=embed)
        else:
            raise

    @commands.command(name="avatar")
    async def _avatar(self, ctx, *, member: discord.Member = None):
        '''
        Get the avatar of the given member
        '''
        if member:
            await ctx.send(member.avatar_url)
        else:
            await ctx.send(ctx.author.avatar_url)

    @commands.command(name="pixel", aliases=["pixelate"])
    async def _pixelate(self, ctx, *, member: discord.Member):
        '''
        Pixelate the given member
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.pixel(), url)
            file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="colours", aliases=["colors"])
    async def _colours(self, ctx, *, member: discord.Member):
        '''
        Analyse the colours of the given member
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.colors(), url)
            file = discord.File(fp=img.image, filename=f"colours.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="wanted", aliases=["want"])
    async def _wanted(self, ctx, *, member: discord.Member):
        '''
        Just like in the wild west
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.wanted(), url)
            file = discord.File(fp=img.image, filename=f"wanted.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="triggered", aliases=["trigger"])
    async def _triggered(self, ctx, *, member: discord.Member):
        '''
        REEEE
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.triggered(), url)
            file = discord.File(
                fp=img.image, filename=f"triggered.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="america")
    async def _america(self, ctx, *, member: discord.Member):
        '''
        Good ol' america
        '''
        await ctx.send("Please wait, this may take some time")
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.america(), url)
            file = discord.File(fp=img.image, filename=f"america.{img.format}")
            await ctx.send(f"{ctx.author.mention}", file=file)

    @commands.command(name="wasted")
    async def _wasted(self, ctx, *, member: discord.Member):
        '''
        GTA but in discord
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.wasted(), url)
            file = discord.File(fp=img.image, filename=f"wasted.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="invert")
    async def _invert(self, ctx, *, member: discord.Member):
        '''
        Invert the picture
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.invert(), url)
            file = discord.File(fp=img.image, filename=f"invert.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="triangle")
    async def _triangle(self, ctx, *, member: discord.Member):
        '''
        Triangles
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.triangle(), url)
            file = discord.File(fp=img.image, filename=f"triangle.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="hog")
    async def _hog(self, ctx, *, member: discord.Member):
        '''
        Not really sure about this one either
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.hog(), url)
            file = discord.File(fp=img.image, filename=f"hog.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="blur")
    async def _blur(self, ctx, *, member: discord.Member):
        '''
        Forgotten your glasses?
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.blur(), url)
            file = discord.File(fp=img.image, filename=f"blur.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="rgb")
    async def _rgb(self, ctx, *, member: discord.Member):
        '''
        Analyse the rgb
        '''
        await ctx.send("Please wait, this may take some time")
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.rgb(), url)
            file = discord.File(fp=img.image, filename=f"rgb.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="obama")
    async def _obama(self, ctx, *, member: discord.Member):
        '''
        The man the myth the legend
        '''
        await ctx.send("Please wait, this may take some time")
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.obama(), url)
            file = discord.File(fp=img.image, filename=f"obama.{img.format}")
            await ctx.send(file=file)
            
    @commands.command(name="jail")
    async def _jail(self, ctx, *, member: discord.Member):
        '''
        You have been jailed
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.jail(), url)
            file = discord.File(fp=img.image, filename=f"jail.{img.format}")
            await ctx.send(file=file)
            
    @commands.command(name="gay")
    async def _gay(self, ctx, *, member: discord.Member):
        '''
        Pride
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.gay(), url)
            file = discord.File(fp=img.image, filename=f"gay.{img.format}")
            await ctx.send(file=file)
            
    @commands.command(name="deepfry")
    async def _deepfry(self, ctx, *, member: discord.Member):
        '''
        Like chips
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.deepfry(), url)
            file = discord.File(fp=img.image, filename=f"deepfry.{img.format}")
            await ctx.send(file=file)

    @commands.command(name="ascii")
    async def _ascii(self, ctx, *, member: discord.Member):
        '''
        Your image, but ascii
        '''
        with ctx.channel.typing():
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.dagpiclient.image_process(ImageFeatures.ascii(), url)
            file = discord.File(fp=img.image, filename=f"ascii.{img.format}")
            await ctx.send(file=file)
    
def setup(bot):
    bot.add_cog(Images(bot))
