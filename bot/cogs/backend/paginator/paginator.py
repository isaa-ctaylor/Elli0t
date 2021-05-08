import asyncio
from collections import namedtuple
from typing import List, Optional, Union

import discord
from discord.ext import commands
import traceback as tb

input = namedtuple("input", ["content", "picture"])

class paginator(object):
    def __init__(self, ctx, **kwargs):
        self.embeds = None
        self.ctx = ctx
        self.bot = ctx.bot
        self.timeout = int(kwargs.pop("timeout", 60))
        self.current_page = 0
        self.emojis = []
        self.commands = []
        self.footer = kwargs.pop("footer", False)
        self.remove_reactions = True
        self.two_way_reactions = kwargs.pop("two_way_reactions", True)
        self.msg = None
        self.clear()

    def clear(self):
        self.emojis = []
        self.commands = []
        self.current_page = 0

    def add_reaction(self, emoji, command: str):
        self.emojis.append(emoji)
        self.commands.append(command)

    def insert_reaction(self, index: int, emoji, command: str):
        self.emojis.insert(index, emoji)
        self.commands.insert(index, command)

    def remove_reaction(self, emoji):
        for emoji in self.emojis:
            index = self.emojis.index(emoji)
            self.emojis.remove(emoji)
            self.commands.pop(index)

    def remove_reaction_at(self, index):
        if index > len(self.emojis) - 1 or index == -1:
            index = len(self.emojis) - 1
        elif index < 0:
            index = 0
        try:
            self.emojis.pop(index)
            self.commands.pop(index)
        except:
            pass

    async def clear_msg_reactions(self, msg):
        try:
            await msg.clear_reactions()
        except (discord.HTTPException, discord.Forbidden):
            for emoji in self.emojis:
                try:
                    await msg.clear_reaction(emoji)
                except (discord.HTTPException, discord.Forbidden):
                    try:
                        await msg.remove_reaction(emoji, self.ctx.bot.user)
                    except (discord.HTTPException, discord.Forbidden):
                        pass

    async def remove_msg_reaction(self, msg, emoji, user):
        try:
            await msg.remove_reaction(emoji, user)
        except (discord.HTTPException, discord.Forbidden):
            pass

    async def wait_for(self, msg, check, timeout):
        if self.two_way_reactions:
            done, pending = await asyncio.wait([
                self.ctx.bot.wait_for(
                    "reaction_add", check=check),
                self.ctx.bot.wait_for(
                    "reaction_remove", check=check)
            ], return_when=asyncio.FIRST_COMPLETED, timeout=timeout)
            if not done:
                raise asyncio.TimeoutError
            try:
                reaction, user = done.pop().result()
            except asyncio.TimeoutError:
                await self.clear_msg_reactions(msg)
                self.clear()
            for future in done:
                future.exception()
            for future in pending:
                future.cancel()
            else:
                return reaction, user
        else:
            try:
                reaction, user = await self.ctx.bot.wait_for(
                    "reaction_add", check=check, timeout=timeout)
            except asyncio.TimeoutError:
                await self.clear_msg_reactions(msg)
                self.clear()
            else:
                return reaction, user

    async def edit(self, msg, emoji, user, embed=None, file=None):
        if self.remove_reactions:
            await self.remove_msg_reaction(msg, emoji, user)
        if embed:
            await msg.edit(embed=embed, file=file)
        else:
            await msg.edit(embed=(self.embeds[self.current_page].content.set_footer(text=f"{self.current_page + 1}/{len(self.embeds)}", icon_url=user.avatar.url)) if self.footer else self.embeds[self.current_page].content)

    async def send(self, embeds: List[input], send_to: Optional[Union[commands.Context, discord.Member, discord.User]] = None):
        self.embeds = embeds
        
        def check(reaction, user):
            return user == wait_for and reaction.message.id == self.msg.id and str(reaction.emoji) in [*self.emojis, "\U000023f9"]
    
        send_to = send_to or self.ctx
        
        wait_for = self.ctx.author if send_to == self.ctx else send_to
        
        if len(self.embeds) == 0:
            return
        
        if len(self.embeds) == 1:
            try:
                self.msg = await send_to.send(embed=self.embeds[0].content, file=self.embeds[0].picture)
                await self.msg.add_reaction("\U000023f9")
                r, u = await self.bot.wait_for("reaction_add", check=check)
                if str(r.emoji) == "\U000023f9":
                    await self.msg.delete()
                    return
            except Exception as e:
                await self.ctx.send(e)
        
        self.current_page = 0

        if self.footer:
            self.embeds[0].content.set_footer(
                text=f"{self.current_page + 1}/{len(self.embeds)}", icon_url=wait_for.avatar.url)

        self.msg = await send_to.send(embed=self.embeds[0].content, file=self.embeds[0].picture)

        for emoji in self.emojis:
            await self.msg.add_reaction(emoji)
            await asyncio.sleep(0.25)

        self.msg = await self.msg.channel.fetch_message(self.msg.id)

        navigating = True

        while navigating:
            if self.timeout > 0:
                try:
                    reaction, user = await self.wait_for(self.msg, check, self.timeout)
                except (TypeError, asyncio.TimeoutError):
                    await self.clear_msg_reactions(self.msg)
                    navigating = False
            else:
                try:
                    reaction, user = await self.wait_for(self.msg, check, None)
                except (TypeError, asyncio.TimeoutError):
                    await self.clear_msg_reactions(self.msg)
                    navigating = False

            try:
                index = self.emojis.index(reaction.emoji)

                command = self.commands[index]
            except:
                pass
            else:
                if command == "first":
                    self.current_page = 0
                    await self.edit(self.msg, reaction.emoji, user)

                elif command == "back":
                    if self.current_page == 0:
                        pass
                    else:
                        self.current_page -= 1
                    await self.edit(self.msg, reaction.emoji, user)

                elif command in ["lock", "clear", "stop"]:
                    await self.clear_msg_reactions(self.msg)
                    navigating = False

                elif command == "delete":
                    await self.msg.delete()
                    await self.ctx.message.add_reaction("\U00002705")
                    navigating = False

                elif command == "next":
                    if self.current_page == len(self.embeds) - 1:
                        pass
                    else:
                        self.current_page += 1
                    await self.edit(self.msg, reaction.emoji, user)

                elif command == "last":
                    self.current_page = len(self.embeds) - 1
                    await self.edit(self.msg, reaction.emoji, user)

                elif command == "info":
                    embed = discord.Embed(title="Info", description="Seems like you stumbled upon the help page! Use the arrows below to move around the menu!",
                                          colour=self.bot.neutral_embed_colour).set_footer(text=f"Requested by {wait_for.name}#{wait_for.discriminator}", icon_url=user.avatar.url)
                    await self.edit(self.msg, emoji, user, embed)

                elif command == "number":
                    def msgcheck(m):
                        return m.author.id == wait_for.id and m.content in range(1, len(self.embeds))

                    choice_msg = await send_to.send("What page do you want to go to?")

                    m = await self.ctx.bot.wait_for("message", check=msgcheck, timeout=self.timeout or None)

                    self.current_page = int(m.content) - 1
                    await choice_msg.delete()
                    await self.edit(self.msg, reaction.emoji, user)

                elif command == "delete":
                    await self.msg.delete()
                    await self.ctx.message.add_reaction("\U0001f44d")
                    navigating = False