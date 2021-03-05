from __future__ import division

import math
import operator

import discord
import pyparsing
from discord.ext import commands
from pyparsing import (CaselessLiteral, Combine, Forward, Group, Literal,
                       Optional, Word, ZeroOrMore, alphas, nums, oneOf)

from .backend.maths.main import solve


def cmp(a, b):
    return (a > b) - (a < b)


class Maths(commands.Cog):
    '''Can't be bothered to do your maths homework? I'll try help!'''

    def __init__(self, bot):
        self.bot = bot

    async def splitsolve(self, expression, splitby):
        things = expression.split(splitby, 1)

        for num, i in enumerate(things):
            things[num] = await self.solve(i)

        if (type(things[num]) in [int, float]) and type(things[num]) == float and things[num].is_integer():
            things[num] = int(things[num])

        return all(e == things[0] for e in things)

    async def solve(self, expression):
        altered = expression.replace("**", "^")
        altered = altered.replace("\U000000f7", "/")

        # if betterbool(expression) == True:
        #     return "True"

        # if altered.startswith("return "):
        #     return await self.solve(altered[7:len(altered)])

        # if "=" in altered and not "==" in altered:
        #     return await self.splitsolve(altered, "=")

        # elif "==" in altered:
        #     return await self.splitsolve(altered, "==")

        # elif "and" in altered.lower():
        #     return await self.splitsolve(altered, "and")

        answer = await solve(expression)

        if type(answer) in [float] and answer.is_integer():
            answer = int(answer)

        return answer

    @commands.command(name="solve", aliases=["math", "calculate", "calc", "maths"])
    async def _solve(self, ctx, *, expression):
        '''
        Solve a maths equation
        '''

        try:
            answer = await self.solve(expression)

            embed = discord.Embed(colour=discord.Colour.green())
            embed.add_field(name="Input", value=f"```\n{expression}```")
            embed.add_field(name="Output", value=f"```\n{answer}```")
        except Exception as e:
            if isinstance(e, pyparsing.ParseException):
                embed = discord.Embed(
                    title="Error!", colour=discord.Colour.red())
                embed.add_field(name="Input", value=f"```\n{expression}```")
                embed.add_field(
                    name="Error", value=f"```\nUnexpected input \"{e.line}\"```")
            elif isinstance(e, OverflowError):
                embed = discord.Embed(
                    title="Error!", colour=discord.Colour.red())
                embed.add_field(name="Input", value=f"```\n{expression}```")
                embed.add_field(
                    name="Error", value=f"```\nOverflowError```")
            else:
                # raise
                embed = discord.Embed(
                    title="Error!", colour=discord.Colour.red())
                embed.add_field(name="Input", value=f"```\n{expression}```")
                embed.add_field(
                    name="Error", value=f"```\n{str(e)}```")
        finally:
            await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Maths(bot))
