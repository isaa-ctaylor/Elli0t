import discord
from discord.ext import commands
from typing import Optional, List, Union


class Elli0tContext(commands.Context):
    @property
    async def codeblock(self, code: str = None, language: str = None):
        await self.send(f"```{language or ''}\n{code or ''}```")

    cb = codeblock

    @property
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
