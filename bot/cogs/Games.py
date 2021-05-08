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

import asyncio
import random

import discord
import numpy
from discord.ext import commands
from xo import ai
from xo.game import Game

from utils.utils import getItem

expected = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    "delete": "❌"}

coords = {n + 1: (n // 3 + 1, n % 3 + 1) for n in range(9)}

async def getEmoji(thing: str, index: int) -> str:
    if thing == " ":
        return expected[index]
    elif thing == "o":
        return "⭕"
    elif thing == "x":
        return "❌"

async def toEmoji(board: list) -> str:
    string = ""
    suffix = ""
    for i, item in enumerate(board, start=1):
        suffix = "\n" if i % 3 == 0 else " "
        string += f"{await getEmoji(item, int(i))}{suffix}"

    return string

hangman = [
    '''
    ```
    +---+
    |   |
        |
        |
        |
        |
    =========```
    ''',
    '''
    ```
    +---+
    |   |
    O   |
        |
        |
        |
    =========```
    ''',
    '''
    ```
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========```
    ''',
    '''
    ```
    +---+
    |   |
    O   |
    /|   |
        |
        |
    =========```
    ''',
    '''
    ```
    +---+
    |   |
    O   |
    /|\  |
        |
        |
    =========```
    ''',
    '''
    ```
    +---+
    |   |
    O   |
    /|\  |
    /    |
        |
    =========```
    ''',
    '''
    ```
    +---+
    |   |
    O   |
    /|\  |
    / \  |
        |
    =========```
    '''
]

def makestring(letters):
    if len(letters) == 0:
        return "None"
    else:
        return ", ".join(letters)

class Games(commands.Cog):
    '''
    Little minigames to get you competetive
    '''
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name= "tictactoe", aliases = ["ttt"])
    async def _tictactoe(self, ctx, *, opponent: discord.Member = None):
        '''
        Play tic tac toe
        '''
        if opponent == ctx.author:
            return await ctx.reply(embed=discord.Embed(title="Error!", description="You can't play against yourself!", colour=self.bot.bad_embed_colour))

        if opponent:
            def check(reaction, user):
                return (user == opponent) and (str(reaction.emoji) in ["✅", "❎"])

            accept = discord.Embed(title="Tictactoe", description=f"{opponent.mention}, {ctx.author.mention} wants to play tictactoe with you!\nDo you accept?", colour=discord.Colour.green(
            )).set_footer(text="React with ✅ if you want to play, and ❎ if you don't! | Request expires in 60 seconds.", icon_url=opponent.avatar.url)
            msg = await ctx.reply(f"{opponent.mention}", embed=accept)

            await msg.add_reaction("✅")
            await msg.add_reaction("❎")

            try:
                reaction, _user = await self.bot.wait_for('reaction_add', timeout=60, check=check)

            except asyncio.TimeoutError:
                error = discord.Embed(
                    title="Uh oh!", description="Looks like the request expired!", colour=self.bot.bad_embed_colour)
                await msg.edit(content=None, embed=error)

                try:
                    await msg.clear_reactions()

                except discord.errors.HTTPException:
                    pass

            else:
                if str(reaction.emoji) == "✅":
                    await msg.delete()
                    game = Game()

                    game.start("x")

                    board = await toEmoji(game.board.cells)

                    player = random.choice([opponent, ctx.author])

                    xOrO = "⭕" if player == ctx.author else "❌"

                    board_embed = discord.Embed(title="Tic Tac Toe", description=board, colour=discord.Colour.green(
                    ) if player == opponent else self.bot.bad_embed_colour).add_field(name="Player", value=f"{player.mention}: {xOrO}")

                    board_message = await ctx.reply(embed=board_embed, new_message=True)

                    for reaction in expected:
                        await board_message.add_reaction(expected[reaction])

                    def numcheck(reaction, user):
                        return (user == player) and (str(reaction.emoji) in [expected[reaction] for reaction in expected]) and (reaction.message == board_message)

                    while True:
                        while True:
                            while True:
                                try:
                                    number, user = await self.bot.wait_for('reaction_add', check=numcheck, timeout=60.0)
                                except asyncio.TimeoutError:
                                    error = discord.Embed(
                                        title="Uh oh!", description=f"{player.mention} didn't play in time!", colour=self.bot.bad_embed_colour)
                                    await board_message.edit(content=None, embed=error)
                                    try:
                                        return await board_message.clear_reactions()
                                    except discord.errors.HTTPException:
                                        return
                                else:
                                    if not str(number.emoji) == "❌":
                                        for key, time in enumerate(expected, start=1):
                                            if str(number.emoji) == expected[key]:
                                                place = time
                                                break

                                        x, y = coords[place]
                                        
                                        if game.board[x, y] not in ["x", "o"]:
                                            result = game.moveto(x, y)

                                            try:
                                                await number.message.clear_reaction(number.emoji)
                                            except discord.errors.HTTPException:
                                                pass
                                            break
                                        
                                        else:
                                            await ctx.reply("You can't move there!", delete_after=3, new_message=True)
                                    else:
                                        await number.message.delete()
                                        return await ctx.message.add_reaction("\U0001f44d")

                            if result['name'] == 'next-turn':
                                player = opponent if player == ctx.author else ctx.author
                                xOrO = "⭕" if player == ctx.author else "❌"

                                board_embed = discord.Embed(title="Tic Tac Toe", description=await toEmoji(game.board.cells), colour=discord.Colour.green() if player == opponent else self.bot.bad_embed_colour).add_field(name="Player", value=f"{player.mention}: {xOrO}")

                                await board_message.edit(embed=board_embed)

                            elif result['name'] == 'gameover':
                                if result['reason'] == 'winner':
                                    win_embed = discord.Embed(
                                        title="🎉 Winner! 🎉", description=await toEmoji(game.board.cells), colour=discord.Colour.gold()).add_field(name="Winner", value=f"Congrats! {player.mention} won!")
                                    await board_message.edit(embed=win_embed)
                                    try:
                                        return await board_message.clear_reactions()
                                    except discord.errors.HTTPException:
                                        return
                                elif result['reason'] == 'squashed':
                                    draw_embed = discord.Embed(
                                        title="Draw!", description=f"It's a draw!", colour=discord.Colour.blurple())
                                    await board_message.edit(embed=draw_embed)
                                    try:
                                        return await board_message.clear_reactions()
                                    except discord.errors.HTTPException:
                                        return
                elif str(reaction.emoji) == "❎":
                    error = discord.Embed(
                        title="Uh oh!", description=f"Looks like {opponent.mention} didn't want to play!", colour=self.bot.bad_embed_colour)
                    await msg.edit(content=None, embed=error)
                    try:
                        await msg.clear_reactions()
                    except discord.errors.HTTPException:
                        pass
        else:
            game = Game()

            game.start("x")

            board = await toEmoji(game.board.cells)

            player = random.choice([ctx.guild.me, ctx.author])
            
            starter = player

            xOrO = "⭕" if player == ctx.author else "❌"

            board_embed = discord.Embed(title="Tic Tac Toe", description=board, colour=discord.Colour.green(
            ) if player == opponent else self.bot.bad_embed_colour).add_field(name="Player", value=f"{player.mention}: {xOrO}")

            board_message = await ctx.reply(embed=board_embed, new_message=True)

            for reaction in expected:
                await board_message.add_reaction(expected[reaction])

            messageID = board_message.id

            while True:
                if player == ctx.guild.me:
                    if starter == ctx.guild.me:
                        aiMove = ai.evaluate(game.board, "x")
                    else:
                        aiMove = ai.evaluate(game.board, "o")

                    x, y = random.choice(aiMove[2])

                    result = game.moveto(x, y)

                    number = await getItem(coords, (x, y))

                    board_message = await board_message.channel.fetch_message(messageID)

                    for i in board_message.reactions:
                        if str(i.emoji) == expected[int(number)]:
                            try:
                                await board_message.clear_reaction(i)
                            except discord.errors.HTTPException:
                                pass

                    if result['name'] == 'next-turn':
                        player = opponent if player == ctx.author else ctx.author
                        xOrO = "⭕" if player == ctx.author else "❌"

                        board_embed = discord.Embed(title="Tic Tac Toe", description=await toEmoji(game.board.cells), colour=discord.Colour.green() if player == opponent else self.bot.bad_embed_colour).add_field(name="Player", value=f"{player.mention}: {xOrO}")

                        await board_message.edit(embed=board_embed)

                    elif result['name'] == 'gameover':
                        if result['reason'] == 'winner':
                            win_embed = discord.Embed(
                                title="🎉 Winner! 🎉", description=await toEmoji(game.board.cells), colour=discord.Colour.gold()).add_field(name="Winner", value=f"Congrats! {player.mention} won!")
                            await board_message.edit(embed=win_embed)
                            try:
                                return await board_message.clear_reactions()
                            except discord.errors.HTTPException:
                                return
                        elif result['reason'] == 'squashed':
                            draw_embed = discord.Embed(
                                title="Draw!", description=f"It's a draw!", colour=discord.Colour.blurple())
                            await board_message.edit(embed=draw_embed)
                            try:
                                return await board_message.clear_reactions()
                            except discord.errors.HTTPException:
                                return

                def numcheck(reaction, user):
                    return (user == player) and (str(reaction.emoji) in [expected[reaction] for reaction in expected]) and (reaction.message == board_message)

                while True:
                    try:
                        number, user = await self.bot.wait_for('reaction_add', check=numcheck, timeout=60.0)
                    except asyncio.TimeoutError:
                        error = discord.Embed(
                            title="Uh oh!", description=f"{player.mention} didn't play in time!", colour=self.bot.bad_embed_colour)
                        await board_message.edit(content=None, embed=error)
                        try:
                            return await board_message.clear_reactions()
                        except discord.errors.HTTPException:
                            return
                    else:
                        if not str(number.emoji) == "❌":
                            for key, time in enumerate(expected, start=1):
                                if str(number.emoji) == expected[key]:
                                    place = time
                                    break

                            x, y = coords[place]

                            if game.board[x, y] not in ["x", "o"]:
                            
                                result = game.moveto(x, y)

                                try:
                                    await number.message.clear_reaction(number.emoji)
                                except discord.errors.HTTPException:
                                    pass
                                break
                            else:
                                await ctx.reply("You can't move there!", delete_after=3, new_message=True)
                        else:
                            await number.message.delete()
                            return await ctx.message.add_reaction("\U0001f44d")

                if result['name'] == 'next-turn':
                    player = ctx.guild.me if player == ctx.author else ctx.author
                    xOrO = "⭕" if player == ctx.author else "❌"

                    board_embed = discord.Embed(title="Tic Tac Toe", description=await toEmoji(game.board.cells), colour=discord.Colour.green() if player == opponent else self.bot.bad_embed_colour).add_field(name="Player", value=f"{player.mention}: {xOrO}")

                    await board_message.edit(embed=board_embed)

                elif result['name'] == 'gameover':
                    if result['reason'] == 'winner':
                        win_embed = discord.Embed(
                            title="🎉 Winner! 🎉", description=await toEmoji(game.board.cells), colour=discord.Colour.gold()).add_field(name="Winner", value=f"Congrats! You won!" if player == ctx.guild.me else "Haha! I beat you!")
                        await board_message.edit(embed=win_embed)
                        try:
                            return await board_message.clear_reactions()
                        except discord.errors.HTTPException:
                            return
                    elif result['reason'] == 'squashed':
                        draw_embed = discord.Embed(
                            title="Draw!", description=f"It's a draw!", colour=discord.Colour.blurple())
                        await board_message.edit(embed=draw_embed)
                        try:
                            return await board_message.clear_reactions()
                        except discord.errors.HTTPException:
                            return

#     @commands.command(name = "hangman", aliases = ["hm"])
#     async def _hangman(self, ctx):
#         '''
#         Hangman
#         '''
#         won = False
        
#         word = RandomWords().random_word()
        
#         word_len = len(word)
        
#         string = []
        
#         for i in word:
#             if i != " ":
#                 string.append("_")
#             elif i == " ":
#                 string.append("/")
        
#         incorrect = []
        
#         game_embed = discord.Embed(title = "Hangman", description = hangman[0], colour = discord.Colour.blurple())
#         game_embed.add_field(name = "Word", value = f"`{string}`", inline = False)
#         game_embed.add_field(name = "Incorrect", value = makestring(incorrect))
#         game_message = await ctx.reply(embed = game_embed)
        
#         while not won:
#             def check(m):
#                 return (m.author == ctx.author) and (m.channel == ctx.channel) and (len(m.content) == 1)
             
#             try:
#                 message = self.bot.wait_for("message", check = check, timeout = 60)
#             except asyncio.TimeoutError:
#                 error_embed = discord.Embed(title = "Uh oh!", description = "You didn't play in time!", colour = self.bot.bad_embed_colour)
#                 return await game_message.edit(embed = error_embed)
#             else:
#                 if message.content.lower() not in [chr(i) for i in range(92, 122)]:
#                     await ctx.reply("That's not a letter!", delete_after = 2)
#                 else:
#                     if message.content.lower() in string:
#                         indices = [i for i, x in enumerate(
#                             my_list) if x == message.content.lower()]
                        
# #                        for i in 
                    

def setup(bot):
    ''' 
    Adds the cog
    '''
    bot.add_cog(Games(bot))
