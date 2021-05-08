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
from typing import Union

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _register_member(self, member_id, starting_value):
        async with self.bot.db.pool.acquire() as con:
            data = await con.fetch("SELECT eco_enabled FROM userdata WHERE user_id = $1", member_id)

        if data:
            if data[0]["eco_enabled"]:
                raise NameError
            else:
                async with self.bot.db.pool.acquire() as con:
                    await con.execute("UPDATE userdata SET eco_enabled = $1, wallet = $2, bank = $2", True, starting_value)
        else:
            async with self.bot.db.pool.acquire() as con:
                await con.execute("INSERT INTO userdata(user_id, wallet, bank, eco_enabled) values($1, $2, $2, $3) ON CONFLICT (user_id) DO UPDATE SET wallet = $2, bank = $1, eco_enabled = $3 WHERE userdata.user_id = $1", member_id, starting_value, True)

        async with self.bot.db.pool.acquire() as con:
            return (await con.fetch("SELECT wallet, bank, eco_enabled FROM userdata WHERE user_id = $1", member_id))[0]

    async def _check_registered(self, member_id):
        async with self.bot.db.pool.acquire() as con:
            data = await con.fetch("SELECT eco_enabled from userdata WHERE user_id = $1", member_id)

        if data and dict(data[0])["eco_enabled"]:
            return True
        return False

    @commands.command(name="register")
    async def _register(self, ctx):
        try:
            await self._register_member(ctx.author.id, 100)

            embed = discord.Embed(
                title="Done!", description="I have set up a bank account for you!", colour=self.bot.good_embed_colour)
            return await ctx.reply(embed=embed, mention_author=False)
        except NameError:
            embed = discord.Embed(
                title="Error!", description="You already have an account!")
            return await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="unregister")
    async def _unregister(self, ctx):
        if await self._check_registered(ctx.author.id):
            async with self.bot.db.pool.acquire() as con:
                await con.execute("UPDATE userdata SET eco_enabled = $1, wallet = $2, bank = $2 WHERE user_id = $3", False, 0, ctx.author.id)
            embed = discord.Embed(
                title="Done!", description=f"Sad to see you go! If you want to come back, use the `{ctx.prefix}register` command.", colour=self.bot.good_embed_colour)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(
                title="Error!", description=f"You don't have an account! Use the `{ctx.prefix}register` command to make an account", colour=self.bot.bad_embed_colour)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="balance", aliases=["bal"])
    async def _balance(self, ctx, *, member: discord.Member = None):
        member = member if member else ctx.author

        async with self.bot.db.pool.acquire() as con:
            data = await con.fetch("SELECT wallet, bank, eco_enabled FROM userdata WHERE user_id = $1", member.id)

        if data:
            data = dict(data[0])
        else:
            if member.id != ctx.author.id:
                embed = discord.Embed(
                    title="Error!", description="That person doesn't have an account!", colour=self.bot.bad_embed_colour)
                return await ctx.reply(embed=embed, mention_author=False)
            else:
                data = dict(await self._register_member(member.id, 100))
                embed = discord.Embed(
                    description=f"You didnt have an account, so I made one for you", colour=self.bot.good_embed_colour)
                await ctx.reply(embed=embed, mention_author=False)
        if not data["eco_enabled"]:
            if member.id != ctx.author.id:
                embed = discord.Embed(
                    title="Error!", description="That person doesn't have an account!", colour=self.bot.bad_embed_colour)
                return await ctx.reply(embed=embed, mention_author=False)
            else:
                data = dict(await self._register_member(member.id, 100))
                embed = discord.Embed(
                    description=f"You didnt have an account, so I made one for you", colour=self.bot.good_embed_colour)
                await ctx.reply(embed=embed, mention_author=False)

        desc_string = f"**`Wallet:`** {data['wallet'] or 0}\n**`Bank:`** {data['bank'] or '0'}\n**`Total:`** {(data['wallet'] or 0) + (data['bank'] or 0)}"
        embed = discord.Embed(title=f"{member.name}'s balance",
                              description=desc_string, colour=self.bot.neutral_embed_colour)
        embed.set_thumbnail(url=str(member.avatar.url))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="withdraw", aliases=["with"])
    async def _withdraw(self, ctx, *, amount: Union[int, str]):
        if await self._check_registered(ctx.author.id):
            if isinstance(amount, str):
                if amount.lower() == "all":
                    async with self.bot.db.pool.acquire() as con:
                        data = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", ctx.author.id)
                        
                        data = dict(data[0])
                        
                        newwallet = data["wallet"] + data["bank"]
                        newbank = 0
                        
                        await con.execute("UPDATE userdata SET wallet = $1, bank = $2", newwallet, newbank)
                        
                    await self._balance(ctx)
                else:
                    embed = discord.Embed(title="Error!", description=f"`{amount}` isn't an amount I can withdraw!", colour=self.bot.bad_embed_colour)
                    await ctx.reply(embed=embed, mention_author=False)
                    
            elif isinstance(amount, int):
                async with self.bot.db.pool.acquire() as con:
                    data = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", ctx.author.id)
                    
                    data = dict(data[0])
                    
                    if data["bank"] < amount:
                        embed = discord.Embed(title=f"Error!", description=f"You don't have enough coins to do that!", colour=self.bot.bad_embed_colour)
                        return await ctx.reply(embed=embed, mention_author=False)
                    else:
                        newbank = data["bank"] - amount
                        newwallet = data["wallet"] + amount
                        
                        await con.execute("UPDATE userdata SET wallet = $1, bank = $2", newwallet, newbank)
                        
                        await self._balance(ctx)
        else:
            embed = discord.Embed(title="Error!", description=f"You dont have an account! Use the `{ctx.prefix}register` command to make one!", colour=self.bot.bad_embed_colour)
            await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(name="deposit", aliases=["dep"])
    async def _deposit(self, ctx, *, amount: Union[int, str]):
        if await self._check_registered(ctx.author.id):
            if isinstance(amount, str):
                if amount.lower() == "all":
                    async with self.bot.db.pool.acquire() as con:
                        data = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", ctx.author.id)
                        
                        data = dict(data[0])
                        
                        newwallet = 0
                        newbank = data["wallet"] + data["bank"]
                        
                        await con.execute("UPDATE userdata SET wallet = $1, bank = $2", newwallet, newbank)
                        
                    await self._balance(ctx)
                else:
                    embed = discord.Embed(title="Error!", description=f"`{amount}` isn't an amount I can withdraw!", colour=self.bot.bad_embed_colour)
                    await ctx.reply(embed=embed, mention_author=False)
                    
            elif isinstance(amount, int):
                async with self.bot.db.pool.acquire() as con:
                    data = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", ctx.author.id)
                    
                    data = dict(data[0])
                    
                    if data["wallet"] < amount:
                        embed = discord.Embed(title=f"Error!", description=f"You don't have enough coins to do that!", colour=self.bot.bad_embed_colour)
                        return await ctx.reply(embed=embed, mention_author=False)
                    else:
                        newbank = data["bank"] + amount
                        newwallet = data["wallet"] - amount
                        
                        await con.execute("UPDATE userdata SET wallet = $1, bank = $2", newwallet, newbank)
                        
                        await self._balance(ctx)
        else:
            embed = discord.Embed(title="Error!", description=f"You dont have an account! Use the `{ctx.prefix}register` command to make one!", colour=self.bot.bad_embed_colour)
            await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(name="transfer", aliases=["pay"])
    async def _transfer(self, ctx, member: discord.Member, amount: int):
        if await self._check_registered(ctx.author.id) and await self._check_registered(member.id):
            if ctx.author.id == member.id and ctx.author.id != self.bot.owner_id:
                return await ctx.error("You can't give yourself money.", reply=True)
            if amount < 0:
                return await ctx.error("Invalid amount.", reply=True)
            async with self.bot.db.pool.acquire() as con:
                authordata = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", ctx.author.id)
                
                memberdata = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", member.id)

                if authordata and memberdata:
                    authordata = dict(authordata[0])
                    memberdata = dict(memberdata[0])
                    
                    if amount > authordata["wallet"] and ctx.author.id != self.bot.owner_id:
                        embed = discord.Embed(title="Error!", description="You don't have enough coins to do that!", colour=self.bot.bad_embed_colour)
                        return await ctx.reply(embed=embed, mention_author=False)
                    else:
                        newauthorwallet = authordata["wallet"]
                        if not ctx.author.id == self.bot.owner_id:
                            newauthorwallet = authordata["wallet"] - amount
                        newmemberwallet = memberdata["wallet"] + amount
                        
                        await con.execute("UPDATE userdata SET wallet = $1 WHERE user_id = $2", newauthorwallet, ctx.author.id)
                        await con.execute("UPDATE userdata SET wallet = $1 WHERE user_id = $2", newmemberwallet, member.id)
                        
                        embed = discord.Embed(title="Done!", description=f"You successfully payed {member.mention} `{amount}` coins!", colour=self.bot.good_embed_colour)
                        return await ctx.reply(embed=embed, mention_author=False)
        else:
            async with self.bot.db.pool.acquire() as con:
                authordata = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", ctx.author.id)
                
                memberdata = await con.fetch("SELECT wallet, bank FROM userdata WHERE user_id = $1", member.id)
            
            if not authordata:
                embed = discord.Embed(title="Error!", description="You do not have an account!", colour=self.bot.bad_embed_colour)
            else:
                embed = discord.Embed(title="Error!", description=f"{member.mention} does not have an account!", colour=self.bot.bad_embed_colour)
            await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(name="rob", aliases=["steal"])
    async def _rob(self, ctx, member: discord.Member):
        pass
    
def setup(bot):
    bot.add_cog(Economy(bot))
