import discord
from discord.ext import commands
import json

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "../json/data.json")

class AutoSetup(commands.Cog):
    '''
    Automatic setup
    '''
    def __init__(self, bot):
        self.bot=bot


    @commands.Cog.listener(name = "on_guild_join")
    async def _add_server_data(self, guild):
        '''
        Called when the bot joins a guild
        '''
        with open(filename, "r") as f:
            data = json.load(f)
            
        data["servers"][str(guild.id)] = {
            "name": str(guild.name),
            "prefix": "-",
            "filter": {
                "enabled": false,
                "mode": 1,
                "custom": []
            },
            "utility": {
                "join_messages": false
            }
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent = 4)
            
        if guild.system_channel:
            hello_embed = discord.Embed(title = "Hi there!", description = f"Hi there! I'm Elli0t, type `-help` for more info!", colour = discord.Colour.random())
            await guild.system_channel.send(embed = hello_embed)
            
            
    @commands.Cog.listener(name = "on_guild_leave")
    async def _add_server_data(self, guild):
        '''
        Called when the bot leaves a guild
        '''
        with open(".json/data.json", "r") as f:
            data = json.load(f)
            
        del data["servers"][str(guild.id)]
        
        with open("./json/data.json", "w") as f:
            json.dump(data, f, indent = 4)
            
    @commands.Cog.listener(name = "on_guild_update")
    async def _keep_server_name_updated(self, before, after):
        if before.name != after.name:
            with open("./json/data.json", "r") as f:
                data = json.load(f)
            
            data["servers"][str(after.id)]["name"] = str(after.name)
        
            with open("./json/data.json", "w") as f:
                json.dump(data, f, indent = 4)
                
    @commands.Cog.listener(name="on_message_edit")
    async def _reinvoke_commands(self, before, after):
        await self.bot.process_commands(after)


def setup(bot):
    bot.add_cog(AutoSetup(bot))