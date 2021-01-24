import discord
import aiohttp
import asyncio
from discord.ext import commands

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chatting = []

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
            
            payload = {"text": text, "context": context}
            
            async with ctx.channel.typing(), self.bot.session.post("https://public-api.travitia.xyz/talk", json=payload, headers={"authorization": "bpKwHiH'!G$:#;K*<!MO"}) as req:
                response = (await req.json())["response"]

            await ctx.reply(response, mention_author = False)
            
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
                            return await message.reply("Bye!", mention_author = False)

                    payload = {"text": text, "context": context}

                    async with ctx.channel.typing(), self.bot.session.post("https://public-api.travitia.xyz/talk", json=payload, headers={"authorization": "bpKwHiH'!G$:#;K*<!MO"}) as req:
                        response = (await req.json())["response"]
                    
                    await message.reply(response, mention_author = False)
                    
                    context = [text, response]

def setup(bot):
    '''
    Adds the cog
    '''
    bot.add_cog(Chatbot(bot))
