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

from __future__ import division

import discord
from discord.ext import commands
from jishaku.functools import executor_function
from mathjspy import MathJS as MathsJS


def cmp(a, b):
    return (a > b) - (a < b)


class Maths(commands.Cog):
    '''Can't be bothered to do your maths homework? I'll try help!'''

    def __init__(self, bot):
        self.bot = bot
        self.vars = {}
        
    @executor_function
    def _do_solve(self, expression, user_vars):
        expression = expression.replace("**", "^")
        maths = MathsJS()
        for i in user_vars:
            maths.set(i, user_vars[i])  
        return maths.eval(expression)

    @commands.command(name="solve", aliases=["math", "calculate", "calc", "maths"])
    async def _solve(self, ctx, *, expression):
        '''
        Solve a maths equation
        '''
        user_vars = {}
        if ";" in expression:
            parts = expression.split(";")
            if "," in parts[0]:
                variables = parts[0].split(",")
            else:
                variables = [parts[0]]
            

            for var in variables:
                thing1, thing2 = var.split("=")
                user_vars[thing1] = thing2

            expression = parts[-1]
                
        try:
            answer = await self._do_solve(expression, user_vars)
            
            embed = discord.Embed(colour=self.bot.good_embed_colour)
            embed.add_field(name="Input", value=f"```\n{expression}```")
            embed.add_field(name="Output", value=f"```\n{answer}```")
        except Exception as e:
            if isinstance(e, OverflowError):
                embed = discord.Embed(
                    title="Error!", colour=self.bot.bad_embed_colour)
                embed.add_field(name="Input", value=f"```\n{expression.strip()}```")
                embed.add_field(
                    name="Error", value=f"```\nOverflowError```")
            else:
                if isinstance(e, AttributeError):
                    embed = discord.Embed(
                        title="Error!", colour=self.bot.bad_embed_colour)
                    embed.add_field(name="Input", value=f"```\n{expression.strip()}```")
                    embed.add_field(
                        name="Error", value=f"```\n{str(e).split(' in')[0]}```")
                else:
                    embed = discord.Embed(
                        title="Error!", colour=self.bot.bad_embed_colour)
                    embed.add_field(
                        name="Input", value=f"```\n{expression.strip()}```")
                    embed.add_field(
                        name="Error", value=f"```\n{str(e).strip()}```")
        finally:
            await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Maths(bot))
