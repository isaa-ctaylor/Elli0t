import discord
import requests
import json
from discord.ext import commands
import random


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.group(name = "minecraft", aliases = ["mc"])
    async def minecraft(self, ctx):
        if not ctx.invoked_subcommand:
            help_embed = discord.Embed(title = "Minecraft", description = "Minecraft commands, use command `help minecraft`", colour = random.randint(0x000000, 0xFFFFFF))
            await ctx.send(embed = help_embed)

    @minecraft.command(name = "mcplayerinfo", aliases = ["info", "playerinfo"])
    async def _mcplayerinfo(self, ctx, user):
        try:
            user_info = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user}").json()
            uuid = user_info['id']

        except KeyError:
            user_info = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
            uuid = user_info['id']

        skin = f"https://visage.surgeplay.com/full/{str(uuid)}"

        mcinfo_embed = discord.Embed(title = f"{user_info['name']}", colour = random.randint(0x000000, 0xFFFFFF))
        mcinfo_embed.add_field(name = "Username", value = f"`{user_info['name']}`")
        mcinfo_embed.add_field(name = "UUID", value = f"`{uuid}`", inline = True)
        mcinfo_embed.add_field(name = "NameMC Link", value = f"Click [here](https://namemc.com/profile/{user_info['name']})", inline = False)
        raw_names = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()

        sanitised_names = []

        for name in raw_names:
            sanitised_names.append(f"`{name['name']}`")

        sanitised_names = sanitised_names[::-1]

        sanitised_names = "\n".join(sanitised_names)

        mcinfo_embed.add_field(name = "Past usernames", value = f"{sanitised_names}")
        mcinfo_embed.set_thumbnail(url = skin)
        
        await ctx.send(embed = mcinfo_embed)

    @minecraft.command(name = "skin")
    async def _skin(self, ctx, user):
        try:
            user_info = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user}").json()
            uuid = user_info['id']

        except KeyError:
            user_info = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
            uuid = user_info['id']

        skin_embed = discord.Embed(title = f"{user_info['name']}'s skin", colour = random.randint(0x000000, 0xFFFFFF))
        skin_embed.set_image(url = f"https://visage.surgeplay.com/full/{str(uuid)}")
        skin_embed.add_field(name = "Download", value = f"Download {user_info['name']}'s skin [here](https://visage.surgeplay.com/skin/{str(uuid)})")
        await ctx.send(embed = skin_embed)

    @minecraft.command(name = "mojangstatus", aliases = ["mjs", "mojang"])
    async def _mojangstatus(self, ctx):
        mojang_status = requests.get("https://status.mojang.com/check").json()

        status = []
        
        status.append(mojang_status[0]['minecraft.net'])
        status.append(mojang_status[1]['session.minecraft.net'])
        status.append(mojang_status[2]['account.mojang.com'])
        status.append(mojang_status[3]['authserver.mojang.com'])
        status.append(mojang_status[4]['sessionserver.mojang.com'])
        status.append(mojang_status[5]['api.mojang.com'])
        status.append(mojang_status[6]['textures.minecraft.net'])
        status.append(mojang_status[7]['mojang.com'])

        for link in range(len(status)):
            if status[link] == "green":
                status[link] = "🟢"
            elif status[link] == "yellow":
                status[link] = "🟡"
            elif status[link] == "red":
                status[link] = "🔴"

        status_embed = discord.Embed(title = "Mojang status", colour = discord.Colour.red())

        status_embed.add_field(name = "minecraft.net status", value = status[0], inline = True)
        status_embed.add_field(name = "session.minecraft.net status", value = status[1], inline = True)
        status_embed.add_field(name = "account.mojang.com status", value = status[2], inline = True)
        status_embed.add_field(name = "authserver.mojang.com status", value = status[3], inline = True)
        status_embed.add_field(name = "sessionserver.mojang.com status", value = status[4], inline = True)
        status_embed.add_field(name = "api.mojang.com status", value = status[5], inline = True)
        status_embed.add_field(name = "textures.minecraft.net status", value = status[6], inline = True)
        status_embed.add_field(name = "mojang.com status", value = status[7], inline = True)

        status_embed.set_thumbnail(url = "https://www.minecraft.net/content/dam/franchise/logos/Mojang-Studios-Logo-Redbox.jpg")

        await ctx.send(embed = status_embed)

def setup(bot):
    bot.add_cog(Minecraft(bot))