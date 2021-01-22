import discord
from discord.ext import commands


class Links(commands.Cog):
    '''
    A couple helpful links
    '''
    def __init__(self, bot):
        self.bot=bot


    @commands.command(name = "github", aliases = ["source", "git", "code"])
    async def _github(self, ctx):
        '''
        Find the source code on github
        ''' 
        github_embed = discord.Embed(title = "Github", description = f"Find the source code [here](https://www.github.com/isaa-ctaylor/Elli0t/)")
        github_embed.set_thumbnail(url = "https://avatars1.githubusercontent.com/u/9919")
        await ctx.send(embed = github_embed)
    
    @commands.command(name = "ko-fi", aliases = ["coffee", "donate"])
    async def _ko_fi(self, ctx):
        '''
        Buy me a coffee
        '''
        kofi_embed = discord.Embed(title = "Buy me a coffee", description = f"Click [here](https://ko-fi.com/isaa_ctaylor) to buy me a coffee", colour = discord.Colour.random())
        kofi_embed.set_thumbnail(url = "https://storage.ko-fi.com/cdn/useruploads/90f7e47d-7c60-4338-b544-dbf2e6196dca.png")
        await ctx.send(embed = kofi_embed)
    
    @commands.command(name = "support", aliases = ["helpserver"])
    async def _support(self, ctx):
        '''
        Get a link to the support server
        '''
        support_embed = discord.Embed(title = "Support server", description = "Click [here](https://discord.gg/QFmJTNTAry) to join the support server")
        support_embed.set_thumbnail(url = self.bot.user.avatar_url)
        await ctx.send(embed = support_embed)
        
def setup(bot):
    bot.add_cog(Links(bot))