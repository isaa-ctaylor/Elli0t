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

    @commands.group(name = "filter")
    @commands.has_guild_permissions(manage_messages = True)
    async def _filter(self, ctx):
        '''
        Manage the chat filter
        '''
        if not ctx.invoked_subcommand:
            with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
                data = json.load(f)

            mode = "on" if data["servers"][str(ctx.guild.id)]["filter"]["enabled"] == True else "off"

            success_embed = discord.Embed(title = "Chat filter", description = f"The filter is `{mode}`", colour = discord.Colour.green())
            await ctx.reply(embed = success_embed)

    @_filter.command(name = "toggle")
    @commands.has_guild_permissions(manage_messages = True)
    async def _toggle(self, ctx, option = None):
        '''
        Turn the filter on or off
        '''
        with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
                data = json.load(f)

        if option and option.lower() in ["on", "true"]:
            data["servers"][str(ctx.guild.id)]["filter"]["enabled"] = True
        elif option and option.lower() in ["off", "false"]:
            data["servers"][str(ctx.guild.id)]["filter"]["enabled"] = False
        else:
            error_embed = discord.Embed(title = "Error!", description = 'Please enter `on` or `off`' , colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

        with open("/media/Elli0t/Elli0t/bot/json/data.json", "w") as f:
            json.dump(data, f, indent = 4)

        mode = "on" if data["servers"][str(ctx.guild.id)]["filter"]["enabled"] == True else "off"

        success_embed = discord.Embed(title = "Success!", description = f"Turned the filter `{mode}`", colour = discord.Colour.green())
        await ctx.reply(embed = success_embed)

    @_filter.command(name = "mode")
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
            error_embed = discord.Embed(title = "Error!", description = 'Please enter `default` to use the default word list, `custom` to use your server word list or `both` to use both' , colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

        with open("/media/Elli0t/Elli0t/bot/json/data.json", "w") as f:
            json.dump(data, f, indent = 4)

        success_embed = discord.Embed(title = "Success!", description = f"Changed the filter mode to `{mode.lower()}`", colour = discord.Colour.green())
        await ctx.reply(embed = success_embed)

    @_filter.group(name = "custom", aliases = ["words"])
    @commands.has_guild_permissions(manage_messages = True)
    async def _custom(self, ctx):
        '''
        Manage your custom server blacklist
        '''
        if not ctx.invoked_subcommand:
            with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
                data = json.load(f)

            custom_list = data["servers"][str(ctx.guild.id)]["filter"]["custom"]

            words_embed = discord.Embed(title = "Your server's custom words", description = ", ".join(custom_list))
            try:
                await ctx.author.send(embed = words_embed)
                return await ctx.reply(embed = discord.Embed(title = "Done!", description = f"{ctx.author.mention}, check your DMs", colour = discord.Colour.green()))
            except discord.errors.HTTPException:
                return await ctx.reply(embed = discord.Embed(title = "Error!", description = f"{ctx.author.mention}, please enable your DMs!", colour = discord.Colour.red()))


    @_custom.command(name = "add")
    @commands.has_guild_permissions(manage_messages = True)
    async def _add(self, ctx, *, words = None):
        '''
        Add words to your server blacklist
        '''
        if not words:
            error_embed = discord.Embed(title = "Error!", description = "Please enter some words! Seperate the words with `, `")
            return await ctx.reply(embed = error_embed)
        else:
            with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
                data = json.load(f)

            custom_list = data["servers"][str(ctx.guild.id)]["filter"]["custom"]

            words = words.split(", ")

            for word in words:
                if not word in custom_list:
                    custom_list.append(word)

            words = ", ".join(words)

            with open("/media/Elli0t/Elli0t/bot/json/data.json", "w") as f:
                json.dump(data, f, indent = 4)

            success_embed = discord.Embed(title = "Success!", description = f"Successfully added `{words}`")
            await ctx.reply(embed = success_embed, delete_after = 5)

    @_custom.command(name = "remove", aliases = ["delete"])
    @commands.has_guild_permissions(manage_messages = True)
    async def _remove(self, ctx, *, words = None):
        '''
        Remove words from your server blacklist
        '''
        if not words:
            error_embed = discord.Embed(title = "Error!", description = "Please enter some words! Seperate the words with `, `")
            return await ctx.reply(embed = error_embed)

        else:
            with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
                data = json.load(f)

            custom_list = data["servers"][str(ctx.guild.id)]["filter"]["custom"]

            words = words.split(", ")
            no_find = []

            for word in words:
                if word in custom_list:
                    custom_list.pop(custom_list.index(word))
                else:
                    no_find.append(word)

            words = ", ".join(words)
            no_find = ", ".join(no_find)

            with open("/media/Elli0t/Elli0t/bot/json/data.json", "w") as f:
                json.dump(data, f, indent = 4)

            if len(no_find) == 0:
                success_embed = discord.Embed(title = "Success!", description = f"Successfully removed `{words}`")
                await ctx.reply(embed = success_embed, delete_after = 5)
            else:
                error_embed = discord.Embed(title = "Error!", description = f"Couldn't find `{no_find}` in your list of words!", colour = discord.Colour.red())
                await ctx.reply(embed = error_embed, delete_after = 5)

    @commands.Cog.listener(name = "on_message")
    async def remove_words(self, message):
        '''
        Removes messages containing words in the blacklist
        '''
        if message.guild:
            if type(message.author) == discord.Member:
                if message.author.top_role < message.guild.me.top_role:
                    found = False
                    with open("/media/Elli0t/Elli0t/bot/json/data.json", "r") as f:
                        data = json.load(f)

                    enabled = data["servers"][str(message.guild.id)]["filter"]["enabled"]
                    mode = data["servers"][str(message.guild.id)]["filter"]["mode"]
                    default = data["defaults"]["words"]
                    custom = data["servers"][str(message.guild.id)]["filter"]["custom"]

                    if enabled:
                        if mode == 1:
                            for word in default:
                                if word in message.content.lower():
                                    found = True
                                    break
                        elif mode == 2:
                            for word in custom:
                                if word in message.content.lower():
                                    found = True
                                    break
                        elif mode == 3:
                            for word in default:
                                if word in message.content.lower():
                                    found = True
                                    break
                            if not found:
                                for word in custom:
                                    if word in message.content.lower():
                                        found = True
                                        break

                        if found:
                            try:
                                await message.delete()
                                deleted_embed = discord.Embed(title = "Uh oh!", description = f"{message.author.mention}, your message was removed because it contains blacklisted words!", colour = discord.Colour.red())
                                await message.channel.send(message.author.mention, embed = deleted_embed, delete_after = 5)
                            except discord.errors.Forbidden:
                                try:
                                    await message.guild.owner.send("The chat filter cannot be used because I don't have the `manage_messages` perm!")
                                except discord.errors.HTTPException:
                                    pass

    @commands.command(name = "ban", aliases = ["banish"])
    @commands.has_guild_permissions(ban_members = True)
    async def _ban(self, ctx, member: discord.Member, *, reason = "None"):
        '''
        Bans the given user
        '''
        if member.top_role > ctx.author.top_role:
            error_embed = discord.Embed(title = "Error!", description = "You can't punish someone with a higher role than yourself!", colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

        elif member == ctx.author:
            error_embed = discord.Embed(title = "Error!", description = "You can't ban yourself!", colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

        else:
            try:
                await member.ban(reason = reason)
                banned_embed = discord.Embed(title = "Success!", description = f"Successfully banned {member.mention}\nReason: `{reason}`", colour = discord.Colour.green())
                await ctx.reply(embed = banned_embed)
            except discord.errors.Forbidden:
                error_embed = discord.Embed(title = "Error!", description = f"I can't ban {member.mention} because they have a higher role than me!", colour = discord.Colour.red())
                await ctx.reply(embed = error_embed)

    @commands.command(name = "unban", aliases = ["unbanish"])
    @commands.has_guild_permissions(ban_members = True)
    async def _unban(self, ctx, member: discord.Object):
        '''
        Unbans the given user
        '''
        try:
            await ctx.guild.unban(member)
            unbanned_embed = discord.Embed(title = "Success!", description = f"Successfully unbanned {member.mention}", colour = discord.Colour.green())
            return await ctx.reply(embed = unbanned_embed)

        except discord.errors.HTTPException:
            error_embed = discord.Embed(title = "Error!", description = f"Please enter the member id in the format `{self.bot.user.id}`", colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

    @commands.command(name = "mute", aliases = ["shush"])
    @commands.has_guild_permissions(mute_members = True)
    async def _mute(self, ctx, member: discord.Member, *, reason):
        '''
        Mutes the given user
        '''

        if member == ctx.author:
            error_embed = discord.Embed(title = "Error!", description = "You can't mute yourself!", colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

        if (role := discord.utils.get(ctx.guild.roles, name = "Muted")):
            await member.add_roles(role, reason = reason)

            success_embed = discord.Embed(title = "Success!", description = f"Successfully muted {member.mention}\nReason: `{reason}`", colour = discord.Colour.green())
            await ctx.reply(embed = success_embed)
        else:
            role = await ctx.guild.create_role(name = "Muted", reason = "Mute command needs Muted role")
            await member.add_roles(role, reason = reason)
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, read_messages = True, send_messages = False)

            success_embed = discord.Embed(title = "Success!", description = f"Successfully muted {member.mention}\nReason: `{reason}`", colour = discord.Colour.green())
            await ctx.reply(embed = success_embed)

    @commands.command(name = "unmute", aliases = ["unshush"])
    @commands.has_guild_permissions(mute_members = True)
    async def _unmute(self, ctx, member: discord.Member):
        '''
        Unmutes the given user
        '''
        try:
            if (role := discord.utils.get(ctx.guild.roles, name = "Muted")) in member.roles:
                await member.remove_roles(role)
                success_embed = discord.Embed(title = "Success!", description = f"Successfully unmuted {member.mention}", colour = discord.Colour.green())
                await ctx.reply(embed = success_embed)
            else:
                error_embed = discord.Embed(title = "Error!", description = f"{member.mention} hasn't been muted!", colour = discord.Colour.green())
                await ctx.reply(embed = error_embed)
        except ValueError:
            error_embed = discord.Embed(title = "Error!", description = f"{member.mention} hasn't been muted!", colour = discord.Colour.green())
            await ctx.reply(embed = error_embed)
        except discord.errors.Forbidden:
            error_embed = discord.Embed(title = "Error!", description = f"I can't unmute {member.mention} because they have a higher role than me!", colour = discord.Colour.green())
            await ctx.reply(embed = error_embed)

    @commands.command(name = "block")
    @commands.has_guild_permissions(manage_messages = True)
    async def _block(self, ctx, member: discord.Member):
        '''
        Block the given member from speaking in the current channel
        '''
        await ctx.channel.set_permissions(member, send_messages = False)
        success_embed = discord.Embed(title = "Success!", description = f"Blocked {member.mention} from speaking in this channel", colour = discord.Colour.green())
        await ctx.reply(embed = success_embed)            
    
    @commands.command(name = "unblock")
    @commands.has_guild_permissions(manage_messages = True)
    async def _unblock(self, ctx, member: discord.Member):
        '''
        Unblock the given member so they can speak in the current channel
        '''
        await ctx.channel.set_permissions(member, send_messages = True)
        success_embed = discord.Embed(title = "Success!", description = f"Unblocked {member.mention}", colour = discord.Colour.green())
        await ctx.reply(embed = success_embed)  
        
    @commands.command(name = "kick", aliases = ["yeet"])
    @commands.has_guild_permissions(kick_members = True)
    async def _kick(self, ctx, member: discord.Member, *, reason = "None"):
        '''
        Kick the given member
        '''
        if member.top_role > ctx.author.top_role:
            error_embed = discord.Embed(title = "Error!", description = "You can't punish someone with a higher role than yourself!", colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)
        
        await member.kick(reason = reason)
        success_embed = discord.Embed(title = "Success!", description = f"Kicked {member.mention}\nReason: {reason}", colour = discord.Colour.green())
        await ctx.reply(embed = success_embed)
    
def setup(bot):
    bot.add_cog(Moderation(bot))
