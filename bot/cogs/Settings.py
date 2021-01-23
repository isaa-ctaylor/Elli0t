import discord
from discord.ext import commands
import json


class Settings(commands.Cog):
    '''Settings for your guild'''
    def __init__(self, bot):
        self.bot=bot


    @commands.group(name = "settings")
    async def _settings(self, ctx):
        '''
        Settings for your guild
        '''

    @_settings.group(name = "filter")
    @commands.has_guild_permissions(manage_messages = True)
    async def _filter(self, ctx):
        '''
        Manage the chat filter
        '''
        if not ctx.invoked_subcommand:
            with open(filename, "r") as f:
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
        with open(filename, "r") as f:
                data = json.load(f)

        if option and option.lower() in ["on", "true"]:
            data["servers"][str(ctx.guild.id)]["filter"]["enabled"] = True
        elif option and option.lower() in ["off", "false"]:
            data["servers"][str(ctx.guild.id)]["filter"]["enabled"] = False
        else:
            error_embed = discord.Embed(title = "Error!", description = 'Please enter `on` or `off`' , colour = discord.Colour.red())
            return await ctx.reply(embed = error_embed)

        with open(filename, "w") as f:
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
        with open(filename, "r") as f:
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

        with open(filename, "w") as f:
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
            with open(filename, "r") as f:
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
            with open(filename, "r") as f:
                data = json.load(f)

            custom_list = data["servers"][str(ctx.guild.id)]["filter"]["custom"]

            words = words.split(", ")

            for word in words:
                if not word in custom_list:
                    custom_list.append(word)

            words = ", ".join(words)

            with open(filename, "w") as f:
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
            with open(filename, "r") as f:
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

            with open(filename, "w") as f:
                json.dump(data, f, indent = 4)

            if len(no_find) == 0:
                success_embed = discord.Embed(title = "Success!", description = f"Successfully removed `{words}`")
                await ctx.reply(embed = success_embed, delete_after = 5)
            else:
                error_embed = discord.Embed(title = "Error!", description = f"Couldn't find `{no_find}` in your list of words!", colour = discord.Colour.red())
                await ctx.reply(embed = error_embed, delete_after = 5)

    @_settings.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix):
        '''
        Change the prefix for your server
        '''
        with open(filename, "r") as f:
            data = json.load(f)
            
        data["servers"][str(ctx.guild.id)]["prefix"] = str(prefix)
        
        with open(filename, "w") as f:
            json.dump(data, f, indent = 4)
        
        await ctx.guild.me.edit(nick = f"[{prefix}] Elli0t")
        
        success_embed = discord.Embed(title = "Success!", description = f"Prefix changed to `{prefix}`", colour = discord.Colour.green())
        await ctx.reply(embed = success_embed)
        

def setup(bot):
    bot.add_cog(Settings(bot))