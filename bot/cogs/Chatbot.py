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

from async_cleverbot import Cleverbot, DictContext
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()


class Chatbot(commands.Cog):
    '''
    Well... chat bot
    '''

    def __init__(self, bot):
        self.bot = bot
        self.chatting = []

        self.chatbot = Cleverbot(os.getenv("CLEVERBOT"), context=DictContext())

    def is_chatting(self, author):
        if author in self.chatting:
            return True
        else:
            return False

    @commands.command(name="chat", aliases=["cb"])
    async def _chat(self, ctx, *, text: str):
        '''
        Chat with Elli0t!
        '''
        if not (3 <= len(text) <= 60):
            return await ctx.reply("Text must be longer than 3 chars and shorter than 60.")

        elif self.is_chatting(ctx.author):
            return await ctx.reply(f"You don't need to put `{ctx.prefix}chat` at the start of your sentence!")

        else:
            def check(m):
                return (m.author == ctx.author) and (m.channel == ctx.channel)

            context = []

            self.chatting.append(ctx.author)

            async with ctx.typing():
                response = await self.chatbot.ask(text, ctx.author.id)

                await ctx.reply(response.text, mention_author=False)

            message = False

            while True:
                try:
                    message = await self.bot.wait_for("message", check=check, timeout=60)
                except asyncio.TimeoutError:
                    if message:
                        self.chatting.pop(self.chatting.index(ctx.author))
                        return await message.reply("I'm going now, bye! 👋", mention_author=False)
                    else:
                        self.chatting.pop(self.chatting.index(ctx.author))
                        return await ctx.reply("I'm going now, bye! 👋", mention_author=False)
                else:
                    text = message.content

                    for i in ["bye", "cancel", "i'm going"]:
                        if i in text.lower():
                            self.chatting.pop(self.chatting.index(ctx.author))
                            return await message.reply("Bye!", mention_author=False)

                    async with ctx.typing():
                        response = await self.chatbot.ask(text, ctx.author.id)

                        await message.reply(response.text, mention_author=False)


def setup(bot):
    '''
    Adds the cog
    '''
    bot.add_cog(Chatbot(bot))
