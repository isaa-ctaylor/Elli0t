from .database import database
from .prefix import get_prefix
import aiohttp
import datetime
from .context import Elli0tContext
import discord
from discord.ext import commands
from .logging import logger_setup
import os
from aiozaneapi import Client as zClient

class Elli0t(discord.ext.commands.AutoShardedBot):
    '''
    A class that inherits from discord.ext.commands.AutoShardedBot
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_time = datetime.datetime.utcnow()
        self.session = aiohttp.ClientSession()
        self.loaded_cogs = kwargs.pop("cogs")
        self.db = kwargs.pop("database")
        self.prefixless = False
        self.zaneclient = zClient(os.getenv("AIOZANEAPI"))
        
        self = self.loop.run_until_complete(self.db.updatePrefixes(self))
        
        self = self.loop.run_until_complete(self.db.load_emoji_users(self))
        
    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or Elli0tContext)

    async def close(self):
        '''
        Subclass of close, to confirm shutdown
        '''
        await self.zaneclient.close()
        await self.change_presence(status=discord.Status.offline, activity=None)
        await self.session.close()
        await self.db.pool.close()
        await super().close()
        
    async def load_cogs(self):
        os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
        for cog in self.loaded_cogs:
            try:
                self.load_extension(cog)
            except:
                pass

description = """
Elli0t is a multi-purpose discord bot aiming to make your life easier. He contains many different modules, spanning moderation, fun and games. Elli0t is open-source and all code can be found on github: https://github.com/isaa-ctaylor/Elli0t Any contributions would be welcome!
"""

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.emojis = True
intents.voice_states = True
intents.messages = True
intents.guild_messages = True


bot = Elli0t(
   command_prefix=get_prefix,
   description=description,
   intents=discord.Intents.all(),
   case_insensitive=True,
   activity=discord.Game(name="around while testing"),
   cogs=[
       "cogs.Emojis",
       "cogs.Help",
       "cogs.Links",
       "cogs.Listeners",
       "cogs.Moderation",
       "cogs.Owner",
       "cogs.Errors",
       "cogs.Images",
       "cogs.Chatbot",
       "cogs.Fun",
       "cogs.Utility",
       "cogs.Maths",
       "jishaku"
   ],
   prefixless=False,
   database=database(),
   logger=logger_setup()
   )
