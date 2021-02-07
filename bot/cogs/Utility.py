import functools
import io

import aiohttp
import discord
import PIL
import qrcode
from discord.ext import commands
from requests.utils import quote
from utils.utils import utils

utility = utils()

morse = {
    "a": "._",
    "b": "_...",
    "c": "_._.",
    "d": "_..",
    "e": ".",
    "f": ".._.",
    "g": "__.",
    "h": "....",
    "i": "..",
    "j": ".___",
    "k": "_._",
    "l": "._..",
    "m": "__",
    "n": "_.",
    "o": "___",
    "p": ".__.",
    "q": "__._",
    "r": "._.",
    "s": "...",
    "t": "_",
    "u": ".._",
    "v": "..._",
    "w": ".__",
    "x": "_.._",
    "y": "_.__",
    "z": "__..",
    "1": ".____",
    "2": "..___",
    "3": "...__",
    "4": "...._",
    "5": ".....",
    "6": "_....",
    "7": "__...",
    "8": "___..",
    "9": "____.",
    "0": "_____",
    " ": "/"
}

class Utility(commands.Cog):
    '''All the commands in here are like your utility belt!'''

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop = bot.loop)

    @commands.command(name="ping", aliases=["pong"])
    async def _ping(self, ctx):
        '''
        Table tennis anyone?
        '''
        if ctx.invoked_with.lower() == "ping":
            title = "Pong 🏓"
        else:
            title = "Ping 🏓"
        embed = discord.Embed(
            title=title, description=f"Latency = `{round(self.bot.latency * 1000, 2)}ms`", colour=discord.Colour.random())

        await ctx.send(embed=embed)

    @commands.group(name="qr")
    async def _qr(self, ctx):
        '''
        qr code related commands
        '''
        if not ctx.invoked_subcommand:
            await ctx.send_help(self.bot.get_command("qr"))

    @_qr.command(name="make")
    async def _make(self, ctx, *, message):
        '''
        Create a qr code
        '''
        thing = functools.partial(quote, message, safe="")
        
        encoded = await self.bot.loop.run_in_executor(None, thing)
        
        qr_embed = discord.Embed(title="Here you go!",
                                 colour=discord.Colour.green())
        link = f"http://api.qrserver.com/v1/create-qr-code/?size=256x256&data={encoded}"
        qr_embed.set_image(url=link)
        
        await ctx.send(embed = qr_embed)
        
    @_qr.command(name="read", aliases=["decode"])
    async def _read(self, ctx, code = None):
        '''
        Read a qr code
        '''
        if not code:
            if len(ctx.message.attachments) > 0:
                code = ctx.message.attachments[0].url
            else:
                embed = discord.Embed(title="Error!", description="Please provide a url/attachment", colour=discord.Colour.red())
            
        thing = functools.partial(quote, code, safe="")

        encoded = await self.bot.loop.run_in_executor(None, thing)
        
        raw = await self.session.get(f"https://api.qrserver.com/v1/read-qr-code/?outputformat=json&fileurl={encoded}")
        
        jsonData = await raw.json()
        
        data = jsonData[0]["symbol"][0]["data"]
        
        error = jsonData[0]["symbol"][0]["error"]
        
        if data and not error:
            embed = discord.Embed(title="Successfully decoded!", description=f"`{data}`", colour=discord.Colour.green())
        elif error and not data:
            embed = discord.Embed(title="Error!", description=str(
                error).capitalize(), colour=discord.Colour.red())
        
        await ctx.send(embed=embed)

    @commands.group(name="morsecode", aliases=["morse"])
    async def _morsecode(self, ctx):
        '''
        Morse code related commands
        '''
        if not ctx.invoked_subcommand:
            await ctx.send_help(self.bot.get_command("morsecode"))
            
    @_morsecode.command(name="encode", aliases=["make"])
    async def _encode(self, ctx, *, message):
        '''
        Encode a message into morse code!
        '''
        message.replace(" ", "")
        
        newMessage = []
        
        for i in message:
            try:
                newMessage.append(morse[i.lower()])
            except KeyError:
                newMessage.append(i.lower())
            
        newMessage = " ".join(newMessage)
        
        embed = discord.Embed(title="In morse code, that would be:", description=f"`{newMessage}`", colour=discord.Colour.random())
        
        await ctx.send(embed=embed)

    @_morsecode.command(name="decode", aliases=["break", "crack"])
    async def _decode(self, ctx, *, code):
        '''
        Decode morse code
        '''
        if code.startswith("`") and code.endswith("`"):
            code = code.strip("`")
        
        code = code.split(" ")

        newMessage = []

        for i in code:
            try:
                newMessage.append(await utility.pee(morse, i))
            except KeyError:
                newMessage.append(i.lower())

        try:
            newMessage = "".join(newMessage)
        except:
            pass

        embed = discord.Embed(title="In english, that would be:",
                              description=f"`{newMessage}`", colour=discord.Colour.random())

        await ctx.send(embed=embed)

    @commands.command(name="uptime")
    async def _uptime(self, ctx):
        await ctx.send(**{"embed": discord.Embed(description=f"I've been up for: {__import__('humanize').precisedelta(self.bot.start_time, format='%0.0f')}", colour=discord.Colour.random())})

def setup(bot):
    bot.add_cog(Utility(bot))
