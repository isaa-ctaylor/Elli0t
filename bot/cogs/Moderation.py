import discord
import json
from discord.ext import commands
from cogs.global_functions import get_prefix

class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
        permission = argument.guild_permissions.manage_messages # can change into any permission
        if not permission: # checks if user has the permission
            return argument # returns user object
        else:
            raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
        muted = discord.utils.get(ctx.guild.roles, name="Muted") # gets role object
        if muted in argument.roles: # checks if user has muted role
            return argument # returns member object if there is muted role
        else:
            raise commands.BadArgument("The user was not muted.") # self-explainatory


class Moderation(commands.Cog):
    '''Easy commands for keeping your server clean!'''
    def __init__(self, bot):
        self.bot=bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    @commands.command(name = "filter")
    @commands.has_guild_permissions(manage_messages = True)
    async def _filter(self, ctx, option = None):
        '''Toggle the chat filter

        Parameters
        ----------
        option: str
            Can be "on" or "off"

        Usage
        -----
        filter on/off
        '''
        if option:
            if option.lower() == "on":
                option = True
            elif option.lower() == "off":
                option = False
            else:
                raise ValueError('Please enter "on" or "off"')

        with open("naughty.json", "r") as f:
                naughty = json.load(f)

        if option:
            naughty[str(ctx.guild.id)]["on"] = option

        else:
            naughty[str(ctx.guild.id)]["on"] = not naughty[str(ctx.guild.id)]["on"]

        with open("naughty.json", "w") as f:
            json.dump(naughty, f, indent = 4)

        await ctx.send(f"Filter on: {str(option)}")

    @commands.command(name = "filtermode")
    @commands.has_guild_permissions(manage_messages = True)
    async def _filtermode(self, ctx, mode: int):
        '''Change the mode of the filter. There are three modes:
        1: The default list of naughty words
        2: A custom list of naughty words, requires input
        3: A mixture, all the default words and your custom words too

        Parameters
        ----------
        mode: int
            Can be 1, 2 or 3. Corresponds to the modes above

        Usage
        filtermode 1/2/3
        '''

        with open("naughty.json", "r") as f:
                naughty = json.load(f)

        if mode == 1:
            naughty[str(ctx.guild.id)]["mode"] = 1
        elif mode == 2:
            naughty[str(ctx.guild.id)]["mode"] = 2
        elif mode == 3:
            naughty[str(ctx.guild.id)]["mode"] = 3

        with open("naughty.json", "w") as f:
                json.dump(naughty, f, indent = 4)

        await ctx.send(f"Changed the mode to `{mode}`")

    @commands.command(name = "customadd")
    @commands.has_guild_permissions(manage_messages = True)
    async def _customadd(self, ctx, *, words):
        '''Add custom words to your server's blacklist

        Parameters
        ----------
        words: str
            The words to add, must be seperated by a comma then a space: ", "

        Usage
        -----
        customadd <words>
        '''
        words = words.split(", ")

        with open("naughty.json", "r") as f:
            naughty = json.load(f)
        
        for word in words:
            naughty[str(ctx.guild.id)]["custom"].append(word)

        with open("naughty.json", "w") as f:
            json.dump(naughty, f, indent = 4)

        await ctx.send(f"Added! See your server words using the {get_prefix(ctx.guild.id)}words command")

    @commands.command(name = "words")
    @commands.has_guild_permissions(manage_messages = True)
    async def _words(self, ctx):
        '''Displays the custom words for your server

        Usage
        -----
        words
        '''
        with open("naughty.json", "r") as f:
            naughty = json.load(f)

        words = "None" if len(naughty[str(ctx.guild.id)]["custom"]) == 0 else ", ".join(naughty[str(ctx.guild.id)]["custom"])

        embed = discord.Embed(title = "Your servers custom blacklisted words", description = f"`{words}`", colour = 0xFF0000)

        await ctx.send(embed = embed, delete_after = 15)

    @commands.command(name = "customremove", aliases = ["cr"])
    @commands.has_guild_permissions(manage_messages = True)
    async def _customremove(self, ctx, word):
        with open("naughty.json", "r") as f:
            naughty = json.load(f)

        if word in naughty[str(ctx.guild.id)]["custom"]:
            naughty[str(ctx.guild.id)]["custom"].pop(naughty[str(ctx.guild.id)]["custom"].index(word))
            await ctx.send(f"Removed {word} from your custom words")
        else:
            await ctx.send("Couldn't find that word, please try again")
        
        with open("naughty.json", "w") as f:
            json.dump(naughty, f, indent = 4)
        

    @commands.Cog.listener(name = "on_message")
    async def auto_remove_words(self, message):
        found = False

        with open("naughty.json", "r") as f:
            naughty = json.load(f)

        author = await message.guild.fetch_member(message.author.id)

        if not author.top_role > message.guild.me.top_role:
            if naughty[str(message.guild.id)]["on"] == True:
                if naughty[str(message.guild.id)]["mode"] == 1:
                    if message.content.lower() in naughty["default"]:
                        found = True
                elif naughty[str(message.guild.id)]["mode"] == 2:
                    if message.content.lower() in naughty[str(message.guild.id)]["custom"]:
                        found = True
                elif naughty[str(message.guild.id)]["mode"] == 3:
                    if message.content.lower() in naughty["default"] or message.content.lower() in naughty[str(message.guild.id)]["custom"]:
                        found = True

        if found == True:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message has been removed as it contains blacklisted words.", delete_after = 10)


    @commands.command(name = "ban", aliases=["banish"])
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, user: Sinner=None, reason=None):
        """Bans the given user"""
        
        if not user: # checks if there is a user
            return await ctx.send("You must specify a user")
        
        try: # Tries to ban user
            await user.ban(reason = reason or "None")
            banned_embed = discord.Embed(title = "Success!", description = f"{user.mention} has been successfully banned\nReason: `{reason}`", colour = discord.Colour.green())
            await ctx.send(embed = banned_embed)
        except discord.Forbidden:
            error_embed = discord.Embed(title = f"Error!", description = f"{user.mention} has a higher role than me!\n{user.mention}'s highest role: {user.top_role.mention}\nMy highest role: {user.guild.me.top_role.mention}", colour = discord.Colour.red())
            return await ctx.send(embed = error_embed)

    @commands.command(name = "mute", aliases = ["shush"])
    @commands.has_guild_permissions(mute_members = True)
    async def _mute(self, ctx, user: Sinner, reason=None):
        """Mutes the given user."""
        role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
        if not role: # checks if there is muted role
            try: # creates muted role 
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                    await channel.set_permissions(muted, send_messages=False)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role") # self-explainatory
            await user.add_roles(muted) # adds newly created muted role
            muted_embed = discord.Embed(title = "Success!", description = f"{user.mention} has been successfully muted\nReason: `{reason}`", colour = discord.Colour.green())
            await ctx.send(embed = muted_embed)
        else:
            for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                    await channel.set_permissions(role, send_messages=False)
            await user.add_roles(role) # adds already existing muted role
            muted_embed = discord.Embed(title = "Success!", description = f"{user.mention} has been successfully muted\nReason: `{reason}`", colour = discord.Colour.green())
            await ctx.send(embed = muted_embed)
    
    @commands.command(name = "kick", aliases = ["boot"])
    @commands.has_guild_permissions(kick_members = True)
    async def _kick(self, ctx, user: Sinner=None, reason=None):
        if not user: # checks if there is a user 
            return await ctx.send("You must specify a user")
        
        try: # tries to kick user
            await ctx.guild.kick(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
        except discord.Forbidden:
            error_embed = discord.Embed(title = f"Error!", description = f"{user.mention} has a higher role than me!\n{user.mention}'s highest role: {user.top_role.mention}\nMy highest role: {user.guild.me.top_role.mention}", colour = discord.Colour.red())
            return await ctx.send(embed = error_embed)

    @commands.command(name = "unmute", aliases = ["unshush"])
    @commands.has_guild_permissions(mute_members = True)
    async def _unmute(self, ctx, user: Redeemed):
        """Unmutes a muted user"""
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
        await ctx.send(f"{user.mention} has been unmuted")

    @commands.command(name='unban')
    @commands.has_guild_permissions(ban_members = True)
    async def _unban(self, ctx, *, member: discord.Member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.banned_users

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return await ctx.message.add_reaction("👍")

def setup(bot):
    bot.add_cog(Moderation(bot))
