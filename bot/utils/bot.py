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
import datetime
import json
import os
import zipfile

import aiofile
import aiohttp
import discord
import yaml
from discord.ext import commands

from .context import Elli0tContext
from .database import database
from .logging import logger_setup
from .prefix import get_prefix

dirname = os.path.dirname(__file__)
yamlfilename = os.path.join(dirname, '../config.yaml')

jsonfilename = os.path.join(dirname, '../blacklist.json')

class Elli0t(commands.AutoShardedBot):
    '''
    A class that inherits from discord.ext.commands.AutoShardedBot
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.blacklist = kwargs.pop("blacklist")
        self.start_time = datetime.datetime.utcnow()
        self.session = aiohttp.ClientSession()
        self.loaded_cogs = kwargs.pop("cogs")
        self.db = kwargs.pop("database")
        self.prefixless = False
        embed_config = kwargs.pop("embed_colours", {})
        
        self.good_embed_colour = discord.Colour.from_rgb(*tuple(int(embed_config["embed_good_colour"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))
        self.bad_embed_colour = discord.Colour.from_rgb(*tuple(int(embed_config["embed_bad_colour"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))
        self.neutral_embed_colour = discord.Colour.from_rgb(*tuple(int(embed_config["embed_neutral_colour"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))
        
        self = logger_setup(self)
        
        self = self.loop.run_until_complete(self.db.update_prefixes(self))
        
        self = self.loop.run_until_complete(self.db.load_emoji_users(self))
        
    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or Elli0tContext)

    async def close(self):
        '''
        Subclass of close, to confirm shutdown
        '''
        zippedfile = zipfile.ZipFile(f"{self.loggingfilename}.zip", "w")
        zippedfile.write(self.loggingfilename, compress_type=zipfile.ZIP_DEFLATED)
        zippedfile.close()
        if os.path.exists(self.loggingfilename):
            os.remove(self.loggingfilename)
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

async def get_config():
    async with aiofile.async_open(yamlfilename, "r") as f:
        data = yaml.load(await f.read(), Loader=yaml.SafeLoader)
    
    async with aiofile.async_open(jsonfilename, "r") as f:
        jsondata = json.loads(await f.read())
    
    return data, jsondata

config = asyncio.get_event_loop().run_until_complete(get_config())

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
    #    "cogs.Moderation",
       "cogs.Owner",
       "cogs.Images",
       "cogs.Chatbot",
       "cogs.Fun",
       "cogs.Utility",
       "cogs.Maths",
       "cogs.Google",
       "cogs.Dev",
       "cogs.Statcord",
       "jishaku"
   ],
   prefixless=False,
   database=database(),
   embed_colours=config[0]["embed_colours"],
   blacklist=config[1]
   )
