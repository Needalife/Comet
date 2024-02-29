import discord
from utils import *
from discord.ext import commands

class moderation(commands.GroupCog, name="moderation"):
    def __init__(self,bot = commands.Bot):
        self.bot = bot
    
    @commands.command(name="mod",description="Mods only")
    @commands.has_role("Mod")
    async def mod(self,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Help pannel",description="Moderators Only",color=discord.Color.blurple())
            cursor = EmbedCursor(embed=embed)
            #Moderator help pannel
            cursor.add_row("Command","Syntax","Function",True)
            #add more moderator commands
            cursor.add_row("posts"," ","Get a list of post on the server, do !post help for more post commands")
            cursor.add_row("get-code"," ","Get COMET code on git repo, contact Vally for invite")
            
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="posts")
    @commands.has_role("Mod")
    async def posts(self,ctx):
        guild = ctx.guild
        threads = guild.threads
        
        embed = discord.Embed(title="Post list",color=discord.Color.purple())
        cursor = EmbedCursor(embed=embed)
        
        cursor.add_row("Post","OP's","Forum")
        for thread in threads:
            user = await self.bot.fetch_user(thread.owner_id)
            cursor.add_row(thread.jump_url,user.mention,thread.parent)
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="get-code")
    @commands.has_role("Mod")
    async def get_git_repo(self,ctx):
        await ctx.send("https://github.com/Needalife/Comet")
    
async def setup(bot:commands.Bot):
    await bot.add_cog(moderation(bot))