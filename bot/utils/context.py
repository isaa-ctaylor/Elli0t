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
import asyncio

class Elli0tContext(commands.Context):
    async def codeblock(self, code: str = None, language: str = None):
        await self.send(f"```{language or ''}\n{code or ''}```")

    cb = codeblock

    def _embed(self, **kwargs):
        footertext = kwargs.pop("footertext", None)
        footerurl = kwargs.pop("footerurl")
        
        if footertext:
            return discord.Embed(**kwargs).set_footer(text=footertext, icon_url=footerurl)
        return discord.Embed(**kwargs)
    
    async def embed(self, **kwargs):
        reply = kwargs.pop("reply", False)
        send_to = kwargs.pop("destination", self)
        if reply:
            return await send_to.reply(embed=self._embed(**kwargs))
        else:
            return await send_to.send(embed=self._embed(**kwargs))
        
    async def error(self, message, *, reply = False):
        embed = discord.Embed(title="Error!", description=f"```diff\n- {message}```", colour=self.bot.bad_embed_colour)
        if not reply:
            return await self.send(embed=embed)
        return await self.reply(embed=embed, mention_author=False)
    
    async def send(self, content: str = None, **kwargs):
        new_message = kwargs.pop("new_message", False)
        
        try:
            self.bot.message_cache
        except AttributeError:
            self.bot.message_cache = {}
        
        if not new_message:
            message = self.bot.message_cache.get(self.message.id, None)

            if message:
                return await message.edit(content=content, **kwargs)

        message = await super().send(content, **kwargs)

        if self.author.id == self.bot.owner_id:
            self.bot.message_cache[self.message.id] = message

            async def clear_cached_message():
                await asyncio.sleep(120)
                try:
                    del self.bot.message_cache[self.message.id]
                except KeyError:
                    pass
                
            self.bot.loop.create_task(clear_cached_message())

        return message
    
    async def reply(self, content: str=None, **kwargs):
        new_message = kwargs.pop("new_message", False)

        try:
            self.bot.message_cache
        except AttributeError:
            self.bot.message_cache = {}

        if not new_message:
            message = self.bot.message_cache.get(self.message.id, None)

            if message:
                return await message.edit(content=content, **kwargs)

        message = await super().reply(content, **kwargs)

        if self.author.id == self.bot.owner_id:
            self.bot.message_cache[self.message.id] = message

            async def clear_cached_message():
                await asyncio.sleep(120)
                try:
                    del self.bot.message_cache[self.message.id]
                except KeyError:
                    pass

            self.bot.loop.create_task(clear_cached_message())

        return message

    async def isaac(self):
        return self.bot.get_user(self.bot.owner_id)