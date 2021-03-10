import functools
import time

import aiohttp
import discord
from discord.ext import commands
from requests.utils import quote
import googletrans
from googletrans.constants import LANGUAGES
from jishaku.functools import executor_function
from .backend.paginator.paginator import paginator
from mystbin import Client
from jishaku.codeblocks import codeblock_converter

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
        self.trans = googletrans.Translator()
        self.mystbin = Client()

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
            title=title, colour=discord.Colour.random())

        embed.add_field(
            name="<:discord:817091821078970420> Websocket", value=f"```py\n{round(self.bot.latency * 1000, 2)}ms```")
        embed.add_field(name="<a:typing:813679213520879627> Typing",
                        value=f"```py\nPinging...```", inline=True)
        embed.add_field(name="<:postgresql:817089804843876353> Database", value=f"```py\n{round(await self.bot.db.ping(), 2)}ms```", inline=True)

        start = time.perf_counter()
        m = await ctx.reply(embed=embed, mention_author=False)
        theTime = (time.perf_counter() - start) * 1000
        embed = embed.set_field_at(1, name="<a:typing:813679213520879627> Typing",
                                   value=f"```py\n{round(theTime, 2)}ms```", inline=True)

        await m.edit(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

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

        await ctx.send(embed=qr_embed)

    @_qr.command(name="read", aliases=["decode"])
    async def _read(self, ctx, code=None):
        '''
        Read a qr code
        '''
        if not code:
            if len(ctx.message.attachments) > 0:
                code = ctx.message.attachments[0].url
            else:
                embed = discord.Embed(
                    title="Error!", description="Please provide a url/attachment", colour=discord.Colour.red())

        thing = functools.partial(quote, code, safe="")

        encoded = await self.bot.loop.run_in_executor(None, thing)

        raw = await self.bot.session.get(f"https://api.qrserver.com/v1/read-qr-code/?outputformat=json&fileurl={encoded}")

        jsonData = await raw.json()

        data = jsonData[0]["symbol"][0]["data"]

        error = jsonData[0]["symbol"][0]["error"]

        if data and not error:
            embed = discord.Embed(title="Successfully decoded!",
                                  description=f"`{data}`", colour=discord.Colour.green())
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

        embed = discord.Embed(title="In morse code, that would be:",
                              description=f"`{newMessage}`", colour=discord.Colour.random())

        await ctx.send(embed=embed)

    @_morsecode.command(name="decode", aliases=["break", "crack"])
    async def _decode(self, ctx, *, code):
        '''
        Decode morse code
        '''
        def getkey(dictionary, item):
            for i in dictionary:
                if dictionary[i] == item:
                    return i
            return item

        if code.startswith("`") and code.endswith("`"):
            code = code.strip("`")

        code = code.split(" ")

        newMessage = []

        for i in code:
            try:
                newMessage.append(getkey(morse, i))
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

    @executor_function
    def do_translate(self, message, dest="en", src="auto"):
        return self.trans.translate(message, dest=dest, src=src)

    @executor_function
    def do_define(self, word):
        return self.dict.meaning(word)

    @commands.group(name="translate", aliases=["trans", "transl8"], invoke_without_command=True)
    async def _translate(self, ctx, *, message):
        '''
        Translate a message to english, use "translate to" or "translate from" to translate from or to a specific language
        '''
        if not ctx.invoked_subcommand:
            result = await self.do_translate(message)

            embed = discord.Embed(title="Translated", colour=0x2F3136)
            embed.add_field(
                name=f"Original ({LANGUAGES[result.src].capitalize()})", value=f"```\n{message}```", inline=False)
            embed.add_field(name="Output (English)",
                            value=f"```\n{result.text}```", inline=False)

            await ctx.send(embed=embed)

    @_translate.command(name="to")
    async def _translate_to(self, ctx, destination, *, message):
        '''
        Translate to the specified language
        '''
        result = await self.do_translate(message, dest=destination)

        embed = discord.Embed(title="Translated", colour=0x2F3136)
        embed.add_field(
            name=f"Original ({LANGUAGES[result.src].capitalize()})", value=f"```\n{message}```", inline=False)
        embed.add_field(name=f"Output ({LANGUAGES[result.dest].capitalize()})",
                        value=f"```\n{result.text}```", inline=False)

        await ctx.send(embed=embed)

    @_translate.command(name="from")
    async def _translate_from(self, ctx, source, *, message):
        '''
        Translate from the specified language
        '''
        result = await self.do_translate(message, src=source)

        embed = discord.Embed(title="Translated", colour=0x2F3136)
        embed.add_field(
            name=f"Original ({LANGUAGES[result.src].capitalize()})", value=f"```\n{message}```", inline=False)
        embed.add_field(name=f"Output ({LANGUAGES[result.dest].capitalize()})",
                        value=f"```\n{result.text}```", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="define")
    async def _define(self, ctx, *, word):
        '''
        Define the given word
        '''
        try:
            with ctx.channel.typing():
                embeds = []
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.replace(' ', '%20')}") as responses:
                        jsonresponse = await responses.json()
                if isinstance(jsonresponse, list):
                    for response in jsonresponse:
                        word = response.get("word")
                        phonetics = response.get("phonetics")
                        meanings = response.get("meanings")
                        phoneticstext = phonetics[0].get("text", None)
                        if meanings:
                            if phoneticstext:
                                embed = discord.Embed(
                                    title=word, description=f"```\n{phoneticstext}```", colour=0x2F3136)
                            else:
                                embed = discord.Embed(title=word, colour=0x2F3136)

                            for meaning in meanings:
                                definitions = []
                                for i, definition in enumerate(meaning["definitions"]):
                                    definitions.append(
                                        f"{i+1}) {definition['definition']}")
                                embed.add_field(
                                    name=meaning["partOfSpeech"], value="\n".join(definitions))

                        embeds.append(embed)

                    if len(embeds) == 1:
                        await ctx.send(embed=embeds[0])
                    else:
                        pages = paginator(ctx, remove_reactions=True)
                        pages.add_reaction("\U000023ea", "first")
                        pages.add_reaction("\U000025c0", "back")
                        pages.add_reaction("\U0001f5d1", "delete")
                        pages.add_reaction("\U000025b6", "next")
                        pages.add_reaction("\U000023e9", "last")
                        await pages.send(embeds)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find the word {word}!```", colour=discord.Colour.red())
                    await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Error!", description=f"```diff\n- {e}```", colour=discord.Colour.red())
            await ctx.send(embed=embed)

    @commands.command(name="mystbin")
    async def _mystbin(self, ctx, *, text: codeblock_converter):
        if text[1].strip("\n").startswith("https://mystb.in/") or text[1].strip("\n").startswith("http://mystb.in/"):
            paste = await self.mystbin.get(text[1].strip("\n").strip())
            text = f"```{paste.paste_syntax or ''}\n{paste.paste_content}```"
            embed = discord.Embed(
                title=paste.paste_id, description=text, colour=discord.Colour.teal())
            await ctx.send(embed=embed)
        else:
            paste = await self.mystbin.post(text[1].strip("\n"), syntax=text[0])
            embed = discord.Embed(
                title=paste.paste_id, description=f"```\n{paste.url}```", colour=discord.Colour.teal())
            await ctx.send(embed=embed)
    
    
def setup(bot):
    bot.add_cog(Utility(bot))
