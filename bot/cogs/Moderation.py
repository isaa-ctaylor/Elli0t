import json
import os

import discord
import psycopg2
from discord.ext import commands

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "../json/data.json")


class Moderation(commands.Cog):
    '''
    Useful commands for keeping your server clean!
    '''
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener(name = "on_message")
    async def remove_words(self, message):
        '''
        Removes messages containing words in the blacklist
        '''
        if message.guild:
            if type(message.author) == discord.Member:
                if message.author.top_role < message.guild.me.top_role:
                    found = False
                    with open(filename, "r") as f:
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
    @commands.bot_has_guild_permissions(ban_members = True)
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
    async def _unban(self, ctx, member: discord.Object, *, reason = "None"):
        '''
        Unbans the given user
        '''
        try:
            await ctx.guild.unban(member, reason = reason)
            unbanned_embed = discord.Embed(title = "Success!", description = f"Successfully unbanned {member.mention}", colour = discord.Colour.green())
            return await ctx.reply(embed = unbanned_embed)

        except discord.errors.HTTPException:
            error_embed = discord.Embed(title = "Error!", description = f"Please enter the member id in the format `{self.bot.user.id}`", colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

    @commands.command(name = "mute", aliases = ["shush"])
    @commands.has_guild_permissions(mute_members = True)
    async def _mute(self, ctx, member: discord.Member, *, reason = "None"):
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
    async def _unmute(self, ctx, member: discord.Member, *, reason = "None"):
        '''
        Unmutes the given user
        '''
        try:
            if (role := discord.utils.get(ctx.guild.roles, name = "Muted")) in member.roles:
                await member.remove_roles(role, reason = reason)
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
    async def _block(self, ctx, member: discord.Member, *, reason = "None"):
        '''
        Block the given member from speaking in the current channel
        '''
        await ctx.channel.set_permissions(member, send_messages = False, reason = reason)
        success_embed = discord.Embed(title = "Success!", description = f"Blocked {member.mention} from speaking in this channel", colour = discord.Colour.green())
        await ctx.reply(embed = success_embed)            
    
    @commands.command(name = "unblock")
    @commands.has_guild_permissions(manage_messages = True)
    async def _unblock(self, ctx, member: discord.Member, *, reason = "None"):
        '''
        Unblock the given member so they can speak in the current channel
        '''
        await ctx.channel.set_permissions(member, send_messages = True, reason = reason)
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
