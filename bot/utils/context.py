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
from typing import Optional, List, Union


class Elli0tContext(commands.Context):
    async def codeblock(self, code: str = None, language: str = None):
        await self.send(f"```{language or ''}\n{code or ''}```")

    cb = codeblock

    async def embed(self, *, title: Optional[str] = None, url: Optional[str] = None, description: Optional[str] = None, fields: Optional[List[dict]] = None, colour: Optional[Union[discord.Colour, int]] = 0, footer: Optional[dict] = None, image: Optional[str] = None, thumbnail: Optional[str] = None, author: Optional[dict] = None):
        embed = discord.Embed(title=title, url=url,
                              description=description, colour=colour)

        if fields:
            for field in fields:
                embed.add_field(name=field.get("name", "None"), value=field.get(
                    "value", "None"), inline=field.get("inline", False))

        if footer:
            embed.set_footer(text=footer.get("text", "None"), icon_url=footer.get(
                "icon_url", "https://cdn.discordapp.com/embed/avatars/0.png"))

        if image:
            embed.set_image(url=image)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if author:
            embed.set_author(author.get("name", "None"), url=author.get("url", "https://cdn.discordapp.com/embed/avatars/0.png",
                                                                        icon_url=author.get("icon_url", "https://cdn.discordapp.com/embed/avatars/0.png")))

        await self.send(embed=embed)
        
    async def error(self, message, *, reply = False):
        embed = discord.Embed(title="Error!", description=f"```diff\n- {message}```", colour=self.bot.bad_embed_colour)
        if not reply:
            return await self.send(embed=embed)
        return await self.reply(embed=embed, mention_author=False)