import asyncio
from random_words import RandomWords
import numpy

import discord
from discord.ext import commands

expected = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣"
}

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

def stringify(board):
    '''
    Turns the given dict into a str
    '''
    board_string = ""

    x = 1

    for key in board:
        board_string += board[key]

        if x < 3:
            board_string += " "
            x += 1
        elif x == 3:
            board_string += "\n"
            x = 1

    return board_string

def checkWin(board):
    '''
    Checks if the board is in a win state
    '''
    if board["1"] == board["2"] == board["3"]:
        return True
    elif board["4"] == board["5"] == board["6"]:
        return True
    elif board["7"] == board["8"] == board["9"]:
        return True
    elif board["1"] == board["4"] == board["7"]:
        return True
    elif board["2"] == board["5"] == board["8"]:
        return True
    elif board["3"] == board["6"] == board["9"]:
        return True
    elif board["1"] == board["5"] == board["9"]:
        return True
    elif board["3"] == board["5"] == board["7"]:
        return True
    else:
        return False

def checkDraw(board):
    '''
    Checks if the board is in a draw state
    '''
    for key in expected:
        if board[str(key)] == expected[key]:
            return False

    return True
        
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


    @commands.command(name = "tictactoe", aliases = ["ttt", "tic", "tac", "toe"])
    async def _tictactoe(self, ctx, opponent: discord.Member, timeout: int = 60):
        '''
        Tic Tac Toe... not much else to say
        '''
        if opponent == ctx.author:
            return await ctx.send("You can't play against yourself!")
        if opponent == ctx.guild.me:
            return await ctx.send("You can't play against me! (yet)")
        
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

        def check(reaction, user):
            return (user == opponent) and (str(reaction.emoji) in ["✅", "❎"])

        accept = discord.Embed(title = "Tictactoe", description = f"{opponent.mention}, {ctx.author.mention} wants to play tictactoe with you!\nDo you accept?", colour = discord.Colour.green()).set_footer(text = "React with ✅ if you want to play, and ❎ if you don't! | Request expires in 60 seconds.", icon_url = opponent.avatar_url)
        msg = await ctx.send(f"{opponent.mention}", embed = accept)
        
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")

        try:
            reaction, _user = await self.bot.wait_for('reaction_add', timeout = timeout, check = check)
        except asyncio.TimeoutError:
            error = discord.Embed(title = "Uh oh!", description = "Looks like the request expired!", colour = discord.Colour.red())
            await msg.edit(content = None, embed = error)
            try:
                await msg.clear_reactions()
            except discord.errors.HTTPException:
                pass
        else:
            if str(reaction.emoji) == "✅":
                await msg.delete()
                board = {
                    "1": "1️⃣", "2": "2️⃣", "3": "3️⃣",
                    "4": "4️⃣", "5": "5️⃣", "6": "6️⃣",
                    "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
                }

                board_string = stringify(board)

                player = opponent
                xoro = "⭕" if player == opponent else "❌"

                board_embed = discord.Embed(title = "Tictactoe", description = f"{board_string}", colour = discord.Color.green())
                board_embed.add_field(name = "Player:", value = f"{player.mention}: {xoro}")
                board_message = await ctx.send(embed = board_embed)

                for reaction in reactions:
                    await board_message.add_reaction(reaction)
                
                def numcheck(reaction, user):
                    return (user == player) and (str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]) and (reaction.message == board_message)

                while True:
                    while True:
                        try:
                            number, user = await self.bot.wait_for('reaction_add', check = numcheck, timeout = 60.0)
                        except asyncio.TimeoutError:
                            error = discord.Embed(title = "Uh oh!", description = f"{player.mention} didn't play in time!", colour = discord.Colour.red())
                            await board_message.edit(content = None, embed = error)
                            try:
                                return await board_message.clear_reactions()
                            except discord.errors.HTTPException:
                                return
                            
                        for key, time in enumerate(expected, start = 1):
                            if str(number.emoji) == expected[key]:
                                place = time
                        
                        if board[str(place)] != expected[place]:
                            await ctx.send("That place has already been taken!")
                        else:
                            board[str(place)] = "⭕" if player == opponent else "❌"
                            try:
                                await number.message.clear_reaction(number.emoji)
                            except discord.errors.HTTPException:
                                break
                            else:
                                break
                    
                    if checkWin(board):
                        win_embed = discord.Embed(title = "🎉 Winner! 🎉", description = f"Congrats! {player.mention} won!", colour = discord.Colour.gold())
                        await board_message.edit(embed = win_embed)
                        try:
                            return await board_message.clear_reactions()
                        except discord.errors.HTTPException:
                            return
                        
                    if checkDraw(board):
                        draw_embed = discord.Embed(title = "Draw!", description = f"It's a draw!", colour = discord.Colour.blurple())
                        await board_message.edit(embed = draw_embed)
                        try:
                            return await board_message.clear_reactions()
                        except discord.errors.HTTPException:
                            return
                        
                    else:
                        player = opponent if player == ctx.author else ctx.author
                        xoro = "⭕" if player == opponent else "❌"

                        board_embed = discord.Embed(title = "Tictactoe", description = f"{stringify(board)}", colour = (discord.Colour.green() if player == ctx.author else discord.Colour.red()))
                        board_embed.add_field(name = "Player:", value = f"{player.mention}: {xoro}")
                        await board_message.edit(embed = board_embed)
                        
            
            elif str(reaction.emoji) == "❎":
                error = discord.Embed(title = "Uh oh!", description = f"Looks like {opponent.mention} didn't want to play!", colour = discord.Colour.red())
                await msg.edit(content = None, embed = error)
                try:
                    await msg.clear_reactions()
                except discord.errors.HTTPException:
                    pass
            
            else:
                pass
    
    @commands.command(name = "hangman", aliases = ["hm"])
    async def _hangman(self, ctx):
        '''
        Hangman
        '''
        won = False
        
        word = RandomWords().random_word()
        
        word_len = len(word)
        
        string = []
        
        for i in word:
            if i != " ":
                string.append("_")
            elif i == " ":
                string.append("/")
        
        incorrect = []
        
        game_embed = discord.Embed(title = "Hangman", description = hangman[0], colour = discord.Colour.blurple())
        game_embed.add_field(name = "Word", value = f"`{string}`", inline = False)
        game_embed.add_field(name = "Incorrect", value = makestring(incorrect))
        game_message = await ctx.send(embed = game_embed)
        
        while not won:
            def check(m):
                return (m.author == ctx.author) and (m.channel == ctx.channel) and (len(m.content) == 1)
             
            try:
                message = self.bot.wait_for("message", check = check, timeout = 60)
            except asyncio.TimeoutError:
                error_embed = discord.Embed(title = "Uh oh!", description = "You didn't play in time!", colour = discord.Colour.red())
                return await game_message.edit(embed = error_embed)
            else:
                if message.content.lower() not in [chr(i) for i in range(92, 122)]:
                    await ctx.send("That's not a letter!", delete_after = 2)
                else:
                    if message.content.lower() in string:
                        values = numpy.array(string)
                        searchval = message.content.lower()
                        ii = numpy.where(values == searchval)[0]
                        ii = ii.to
                    

def setup(bot):
    ''' 
    Adds the cog
    '''
    bot.add_cog(Games(bot))
