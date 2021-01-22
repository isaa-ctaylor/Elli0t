import discord
from discord.ext import commands
import asyncio
import json
from utils.global_functions import get_default_prefix, timeInSeconds
import random
import datetime





default_prefix = get_default_prefix()


class Utility(commands.Cog):
    '''All the commands in here are like your utility belt!'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def _invite(self, ctx):
        '''Invite the bot to your server!'''
        embed = discord.Embed(
            title="Invite me!", description="Click [here](https://discord.com/api/oauth2/authorize?client_id=778637164388810762&permissions=8&scope=bot) to add me to your server!")
        await ctx.send(embed=embed)

    @commands.command(name="ping", aliases = ["pong"])
    async def _ping(self, ctx):
        '''Table tennis anyone?'''
        if ctx.invoked_with.lower() == "ping":
            title = "Pong 🏓"
        else:
            title = "Ping 🏓"
        embed = discord.Embed(
            title = title, description=f"Latency = `{round(self.bot.latency * 1000, 2)}ms`", colour = random.randint(0x000000, 0xFFFFFF))

        await ctx.send(embed=embed)

    @commands.command(name="poll")
    async def _poll(self, ctx, amount: int = 2):
        if amount > 9:
            return ctx.send(embed = discord.Embed(title = "Sorry!", description = "You can't have more than 9 options!", colour = discord.Colour.red()))
        
        options = []
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        
        embed = discord.Embed(title=f"It's voting time!",
                              description=f"React with the corresponding number to cast your vote!", 
                              colour=discord.Colour.blue())

        def check(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        question_embed = discord.Embed(title = f"Enter option 1").set_footer(text = "Times out in 60 seconds, enter 'cancel' to cancel")
        msg = await ctx.send(embed = question_embed)
        message = await self.bot.wait_for('message', timeout = 60, check = check)

        if message.content.lower() == "cancel":
            return msg.edit(embed = discord.Embed(title = "Aborted", description = "Poll aborted", colour = discord.Colour.red()))

        else:
            embed.add_field(name = reactions[0], value = message.content)
            options.append(message.content)
        
        for option in range(2, amount):
            question_embed = discord.Embed(title = f"Enter option {option}").set_footer(text = "Times out in 60 seconds, enter 'cancel' to cancel")
            await msg.edit(embed = question_embed)
            message = await self.bot.wait_for('message', timeout = 60, check = check)
            
            if message.content.lower() == "cancel":
                return msg.edit(embed = discord.Embed(title = "Aborted", description = "Poll aborted", colour = discord.Colour.red()))
            
            else:
                embed.add_field(name = reactions[option - 1], value = message.content)
                options.append(message.content)

        time = await ctx.send(embed = discord.Embed(title = "Timeout", description = "Do you want a timeout?"))
        
        def rcheck(reaction, user):
            return (user == opponent) and (str(reaction.emoji) in ["✅", "❎"])
        
        reaction, _user = await self.bot.wait_for('reaction_add', timeout = timeout, check = rcheck)
        
        if str(reaction.emoji) == "✅":
            await title.edit(embed = discord.Embed(title = "Enter timeout", description = "Enter timeout in the format: d h m s, enter 'cancel' to cancel"))
            message = await self.bot.wait_for('message', timeout = 60, check = check)
            
            if message.content.lower() == "cancel":
                return msg.edit(embed = discord.Embed(title = "Aborted", description = "Poll aborted", colour = discord.Colour.red()))
            
            timeout = timeInSeconds(message.content.lower())
            
        else:
            timeout = None
        
        await ctx.message.delete()
        
        if timeout:
            embed.set_footer(
            text=f"Poll by {ctx.author} | Ends at {str(ctx.message.created_at + datetime.timedelta(seconds = sleep))[11:-7]} GMT", icon_url=ctx.author.avatar_url)
        else:
            embed.set_footer(
            text=f"Poll by {ctx.author}", icon_url=ctx.author.avatar_url)
        
        msg = await ctx.send(embed=embed)

        for i in range(0, amount - 1):
            await msg.add_reaction(reactions[i])

        if timeout:
            ended = discord.Embed(title="Poll Ended!", description="This poll has ended. The results are as follows:", colour=discord.Colour.red())
            
            await asyncio.sleep(sleep)

            msg = await ctx.message.channel.fetch_message(msg.id)

            reactions = msg.reactions

            votes = []
            
            for i in range(0, amount - 1):
                votes.append([])

            for reaction in reactions:
                if reaction.emoji in reactions:

                    users = await reaction.users().flatten()

                    for h in users:
                        if h.id != self.bot.user.id:
                            for i, item in enumerate(range(0, amount - 1), start = 0):
                                if str(reaction.emoji) == reactions[i]:
                                    votes[i].append(f"{h.name}#{h.discriminator}")
                                    number = item
                                    break
                    
                    ended.add_field(name=f"People who voted for `{options[number]}`", value=("No-one" if len(options[number]) == 0 else ", ".join(options[number])))

            await msg.clear_reactions()
            await msg.edit(embed=ended)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        '''Called when a Guild is either created by the Client or when the Client joins a guild.

        Parameters
        ----------
        guild: discord.Guild
            The guild that was joined
        '''
        if guild.system_channel is not None:
            await guild.system_channel.send(
                f"Hi there! I'm Elli0t, type `{default_prefix}help` for more info!")

        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        
        with open('naughty.json', 'r') as f:
            naughty = json.load(f)

        prefixes[str(guild.id)] = default_prefix
        naughty[str(guild.id)] = {"on": False, "words": 1, "custom": []}

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        with open('naughty.json', 'w') as f:
            json.dump(naughty, f, indent=4)
        

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        '''Called when a Guild is removed from the Client.

        Parameters
        ----------
        guild: discord.Guild
            The guild that got removed.
        '''
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        with open('naughty.json', 'r') as f:
            naughty = json.load(f)

        prefixes.pop(str(guild.id))
        naughty.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        with open('naughty.json', 'w') as f:
            json.dump(naughty, f, indent=4)

    @commands.command(name = "info", aliases = ["i"])
    async def _info(self, ctx):
        try:
            await ctx.send(f"Name: {self.bot.user.name}\nId: {self.bot.user.id}\nAvatar url: {self.bot.user.avatar_url}")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name = "toggle_join_message")
    @commands.has_guild_permissions(manage_messages = True)
    async def toggle_join_message(self, ctx):
        with open("utility.json", "r") as f:
            utility = json.load(f)
        
        utility[str(ctx.guild.id)] = not utility[str(ctx.guild.id)]

        with open("utility.json", "w") as f:
            json.dump(utility, f, indent = 4)

        await ctx.send(f"Join message: `{utility[str(ctx.guild.id)]}`")

    @commands.Cog.listener(name = "on_member_join")
    async def user_join(self, member):
        with open("utility.json", "r") as f:
            utility = json.load(f)
        
        try:
            if utility[str(member.guild.id)]["user_messages"]:
                if member.guild.system_channel:
                    embed = discord.Embed(title = f"Welcome to {member.guild.name}!", description = f"Welcome {member.mention} to {member.guild.name}!", colour = random.randint(0x000000, 0xFFFFFF))
                    embed.set_thumbnail(url = member.guild.icon_url)
                    await member.guild.system_channel.send(embed = embed)
        except KeyError:
            utility.append(str(member.guild.id))

        with open("utility.json", "w") as f:
            json.dump(utility, f, indent = 4)
        
    @commands.command(name = "say")
    @commands.has_guild_permissions(manage_messages = True)
    async def _say(self, ctx, *, message):
        await ctx.message.delete()
        embed = discord.Embed(title = f"Message from {ctx.author.display_name}#{ctx.author.discriminator}", description = message, colour = random.randint(0x000000, 0xFFFFFF))
        await ctx.send(embed = embed)

    @commands.command(name = "announce")
    @commands.has_guild_permissions(manage_messages = True)
    async def _announce(self, ctx, channel: discord.TextChannel, *, message):
        await ctx.message.delete()
        embed = discord.Embed(title = f"📣 Announcement by {ctx.author.display_name}#{ctx.author.discriminator}", description = message, colour = random.randint(0x000000, 0xFFFFFF))
        await channel.send(embed = embed)

    @commands.command(name = "clear", aliases = ["purge", "c"])
    @commands.has_guild_permissions(manage_messages = True)
    async def _clear(self, ctx, channel: discord.TextChannel, amount: int = 10):
        await channel.purge(limit = amount)
        try:
            await ctx.message.add_reaction("👍")
        except discord.NotFound:
            await ctx.send("Purged!", delete_after = 10)

    @commands.command(name = "delete")
    @commands.has_guild_permissions(manage_messages = True)
    async def _delete(self, ctx, message: discord.Message):
        try:
            await message.delete()
            await ctx.message.add_reaction("👍")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name = "todo", aliases = ["td"])
    @commands.has_guild_permissions(manage_messages = True)
    async def _todo(self, ctx, *, todo):
        await ctx.message.delete()
        embed = discord.Embed(title = "Something needs doing!", description = f"{ctx.author.mention} needs you to `{todo}`!", colour = discord.Colour.green())
        embed.set_footer(text = "React with ✅ to indicate you are doing the job, and 👍 when it's finished!")
        message = await ctx.send(embed = embed)
        
        await message.add_reaction("✅")
        await message.add_reaction("👍")
    
    @commands.command(name = "echo")
    async def _echo(self, ctx, *, message):
        await ctx.send(message)

    @commands.command(name = "userinfo")
    async def _userinfo(self, ctx, user: discord.Member = None):
        if not user:
            user = self.bot.get_member(ctx.author.id)
        
        user_embed = discord.Embed(title = "User info", colour = user.colour)
        user_embed.add_field(name = "ID", value = f"`{user.id}`")
        user_embed.add_field(name = "Name", value = f"`{user.name}#{user.discriminator}`", inline = True)
        if user.status:
            if user.status.online:
                status = "Online"
            elif user.status.offline:
                status = "Offline"
            elif user.status.idle:
                status = "Idle"
            elif user.status.dnd:
                status = "Do Not Disturb"

        if user.desktop_status:
            device = "Desktop"
        elif user.mobile_status:
            device = "Mobile"
        elif user.web_status:
            device = "Web"
        
        user_embed.add_field(name = "Status", value = f"`{status}`")
        user_embed.add_field(name = "Device", value = f"`{device}`")
        user_embed.add_field(name = "Roles", value = ", ".join([role.mention for role in user.roles]))

        await ctx.send(embed = user_embed)


def setup(bot):
    bot.add_cog(Utility(bot))
