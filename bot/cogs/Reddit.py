import discord
import os
from dotenv import load_dotenv
import praw
from discord.ext import commands

load_dotenv()

reddit = praw.Reddit(client_id = os.getenv("REDDIT_ID"), client_secret = os.getenv("REDDIT_SECRET"), user_agent = "Elli0t 1.0 by /u/isaa_ctaylor")

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.group(name = "reddit", aliases = ["r"])
    async def _reddit(self, ctx):
        if not ctx.invoked_subcommand:
            


def setup(bot):
    bot.add_cog(Reddit(bot))