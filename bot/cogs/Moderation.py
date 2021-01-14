import json

import discord
from discord.ext import commands

from utils.global_functions import get_prefix


class Moderation(commands.Cog):
    '''
    Useful commands for keeping your server clean!
    '''
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name = "filter")
    @commands.has_guild_permissions(manage_messages = True)
    async def _filter(self, ctx, option = None):
        '''
        Toggle the chat filter
        '''
        with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
            data = json.load(f)
        
        if option and option.lower() in ["on", "true"]:
            data["servers"][str(ctx.guild.id)]["filter"]["enabled"] = True
        elif option and option.lower() in ["off", "false"]:
            data["servers"][str(ctx.guild.id)]["filter"]["enabled"] = False
        else:
            error_embed = discord.Embed(title = "Error!", description = 'Please enter "on" or "off"' , colour = discord.Colour.red())
            return await ctx.send(embed = error_embed)
        
        with open("/media/Elli0t/Elli0t/bot/json/data.json", "w") as f:
            json.dump(data, f, indent = 4)
        
        mode = "on" if data["servers"][str(ctx.guild.id)]["filter"]["enabled"] == True else "off"
        
        success_embed = discord.Embed(title = "Success!", description = f"Turned the filter {mode}", colour = discord.Colour.green())
        await ctx.send(embed = success_embed)

    @commands.command(name = "mode")
    @commands.has_guild_permissions(manage_messages = True)
    async def _filtermode(self, ctx, mode: str):
        '''
        Change the mode of the filter.
        '''

        with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
            data = json.load(f)

        if mode.lower() == "default":
            data["servers"][str(ctx.guild.id)]["filter"]["mode"] = 1
        elif mode.lower() == "custom":
            data["servers"][str(ctx.guild.id)]["filter"]["mode"] = 2
        elif mode.lower() == "both":
            data["servers"][str(ctx.guild.id)]["filter"]["mode"] = 3
        else:
            error_embed = discord.Embed(title = "Error!", description = 'Please enter "default" to use the default word list, "custom" to use your server word list or "both" to use both' , colour = discord.Colour.red())
            return await ctx.send(embed = error_embed)

        with open("/media/Elli0t/Elli0t/bot/json/data.json", "w") as f:
            json.dump(data, f, indent = 4)

        await ctx.send(f"Changed the mode to `{mode}`")

    # @commands.command(name = "customadd")
    # @commands.has_guild_permissions(manage_messages = True)
    # async def _customadd(self, ctx, *, words):
    #     '''Add custom words to your server's blacklist

    #     Parameters
    #     ----------
    #     words: str
    #         The words to add, must be seperated by a comma then a space: ", "

    #     Usage
    #     -----
    #     customadd <words>
    #     '''
    #     words = words.split(", ")

    #     with open("naughty.json", "r") as f:
    #         naughty = json.load(f)
        
    #     for word in words:
    #         naughty[str(ctx.guild.id)]["custom"].append(word)

    #     with open("naughty.json", "w") as f:
    #         json.dump(naughty, f, indent = 4)

    #     await ctx.send(f"Added! See your server words using the {get_prefix(ctx.guild.id)}words command")

    # @commands.command(name = "words")
    # @commands.has_guild_permissions(manage_messages = True)
    # async def _words(self, ctx):
    #     '''Displays the custom words for your server

    #     Usage
    #     -----
    #     words
    #     '''
    #     with open("naughty.json", "r") as f:
    #         naughty = json.load(f)

    #     words = "None" if len(naughty[str(ctx.guild.id)]["custom"]) == 0 else ", ".join(naughty[str(ctx.guild.id)]["custom"])

    #     embed = discord.Embed(title = "Your servers custom blacklisted words", description = f"`{words}`", colour = 0xFF0000)

    #     await ctx.send(embed = embed, delete_after = 15)

    # @commands.command(name = "customremove", aliases = ["cr"])
    # @commands.has_guild_permissions(manage_messages = True)
    # async def _customremove(self, ctx, word):
    #     with open("naughty.json", "r") as f:
    #         naughty = json.load(f)

    #     if word in naughty[str(ctx.guild.id)]["custom"]:
    #         naughty[str(ctx.guild.id)]["custom"].pop(naughty[str(ctx.guild.id)]["custom"].index(word))
    #         await ctx.send(f"Removed {word} from your custom words")
    #     else:
    #         await ctx.send("Couldn't find that word, please try again")
        
    #     with open("naughty.json", "w") as f:
    #         json.dump(naughty, f, indent = 4)
        

    # @commands.Cog.listener(name = "on_message")
    # async def auto_remove_words(self, message):
    #     found = False

    #     with open("naughty.json", "r") as f:
    #         naughty = json.load(f)

    #     author = await message.guild.fetch_member(message.author.id)

    #     if not author.top_role > message.guild.me.top_role:
    #         if naughty[str(message.guild.id)]["on"] == True:
    #             if naughty[str(message.guild.id)]["mode"] == 1:
    #                 if message.content.lower() in naughty["default"]:
    #                     found = True
    #             elif naughty[str(message.guild.id)]["mode"] == 2:
    #                 if message.content.lower() in naughty[str(message.guild.id)]["custom"]:
    #                     found = True
    #             elif naughty[str(message.guild.id)]["mode"] == 3:
    #                 if message.content.lower() in naughty["default"] or message.content.lower() in naughty[str(message.guild.id)]["custom"]:
    #                     found = True

    #     if found == True:
    #         await message.delete()
    #         await message.channel.send(f"{message.author.mention}, your message has been removed as it contains blacklisted words.", delete_after = 10)


    # @commands.command(name = "ban", aliases=["banish"])
    # @commands.has_permissions(ban_members=True)
    # async def _ban(self, ctx, user: Sinner=None, reason=None):
    #     """Bans the given user"""
        
    #     if not user: # checks if there is a user
    #         return await ctx.send("You must specify a user")
        
    #     try: # Tries to ban user
    #         await user.ban(reason = reason or "None")
    #         banned_embed = discord.Embed(title = "Success!", description = f"{user.mention} has been successfully banned\nReason: `{reason}`", colour = discord.Colour.green())
    #         await ctx.send(embed = banned_embed)
    #     except discord.Forbidden:
    #         error_embed = discord.Embed(title = f"Error!", description = f"{user.mention} has a higher role than me!\n{user.mention}'s highest role: {user.top_role.mention}\nMy highest role: {user.guild.me.top_role.mention}", colour = discord.Colour.red())
    #         return await ctx.send(embed = error_embed)

    # @commands.command(name = "mute", aliases = ["shush"])
    # @commands.has_guild_permissions(mute_members = True)
    # async def _mute(self, ctx, user: Sinner, reason=None):
    #     """Mutes the given user."""
    #     role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
    #     if not role: # checks if there is muted role
    #         try: # creates muted role 
    #             muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
    #             for channel in ctx.guild.channels: # removes permission to view and send in the channels 
    #                 await channel.set_permissions(muted, send_messages=False)
    #         except discord.Forbidden:
    #             return await ctx.send("I have no permissions to make a muted role") # self-explainatory
    #         await user.add_roles(muted) # adds newly created muted role
    #         muted_embed = discord.Embed(title = "Success!", description = f"{user.mention} has been successfully muted\nReason: `{reason}`", colour = discord.Colour.green())
    #         await ctx.send(embed = muted_embed)
    #     else:
    #         for channel in ctx.guild.channels: # removes permission to view and send in the channels 
    #                 await channel.set_permissions(role, send_messages=False)
    #         await user.add_roles(role) # adds already existing muted role
    #         muted_embed = discord.Embed(title = "Success!", description = f"{user.mention} has been successfully muted\nReason: `{reason}`", colour = discord.Colour.green())
    #         await ctx.send(embed = muted_embed)
    
    # @commands.command(name = "kick", aliases = ["boot"])
    # @commands.has_guild_permissions(kick_members = True)
    # async def _kick(self, ctx, user: Sinner=None, reason=None):
    #     if not user: # checks if there is a user 
    #         return await ctx.send("You must specify a user")
        
    #     try: # tries to kick user
    #         await ctx.guild.kick(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
    #     except discord.Forbidden:
    #         error_embed = discord.Embed(title = f"Error!", description = f"{user.mention} has a higher role than me!\n{user.mention}'s highest role: {user.top_role.mention}\nMy highest role: {user.guild.me.top_role.mention}", colour = discord.Colour.red())
    #         return await ctx.send(embed = error_embed)

    # @commands.command(name = "unmute", aliases = ["unshush"])
    # @commands.has_guild_permissions(mute_members = True)
    # async def _unmute(self, ctx, user: Redeemed):
    #     """Unmutes a muted user"""
    #     await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
    #     await ctx.send(f"{user.mention} has been unmuted")

    # @commands.command(name='unban')
    # @commands.has_guild_permissions(ban_members = True)
    # async def _unban(self, ctx, *, member: discord.Member):
    #     banned_users = await ctx.guild.bans()
    #     member_name, member_discriminator = member.split('#')

    #     for ban_entry in banned_users:
    #         user = ban_entry.banned_users

    #         if (user.name, user.discriminator) == (member_name, member_discriminator):
    #             await ctx.guild.unban(user)
    #             return await ctx.message.add_reaction("👍")

def setup(bot):
    bot.add_cog(Moderation(bot))
