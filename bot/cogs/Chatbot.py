import discord
import async_cleverbot as ac
import asyncio
import aiohttp
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
        
        self.chatbot = ac.Cleverbot(os.getenv("CLEVERBOT"), context = ac.DictContext())

    def is_chatting(self, author):
        if author in self.chatting:
            return True
        else:
            return False

    @commands.command(name = "chat", aliases = ["cb"])
    async def _chat(self, ctx, *, text: str):
        '''
        Chat with Elli0t!
        '''
        if not (3 <= len(text) <= 60):
            return await ctx.send("Text must be longer than 3 chars and shorter than 60.")
        
        elif self.is_chatting(ctx.author):
            return await ctx.send(f"You don't need to put `{ctx.prefix}chat` at the start of your sentence!")
        
        else:
            def check(m):
                return (m.author == ctx.author) and (m.channel == ctx.channel)
            
            context = []
            
            self.chatting.append(ctx.author)
            
            response = await self.chatbot.ask(text, ctx.author.id)

            await ctx.reply(response.text, mention_author = False)
            
            message = False
            
            while True:
                try:
                    message = await self.bot.wait_for("message", check = check, timeout = 60)
                except asyncio.TimeoutError:
                    if message:
                        self.chatting.pop(self.chatting.index(ctx.author))
                        return await message.reply("I'm going now, bye! 👋", mention_author = False)
                    else:
                        self.chatting.pop(self.chatting.index(ctx.author))
                        return await ctx.reply("I'm going now, bye! 👋", mention_author = False)
                else:
                    text = message.content
                    
                    if text.startswith(f"{ctx.prefix}chat"):
                        await ctx.send(f"You don't need to put `{ctx.prefix}chat` at the start of your sentence!")
                    
                    for i in ["bye", "cancel", "i'm going"]:
                        if i in text.lower():
                            self.chatting.pop(self.chatting.index(ctx.author))
                            return await message.reply("Bye!", mention_author = False)

                    response = await self.chatbot.ask(text, ctx.author.id)

                    await message.reply(response.text, mention_author = False)

def setup(bot):
    '''
    Adds the cog
    '''
    bot.add_cog(Chatbot(bot))
