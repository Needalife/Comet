import discord
from utils import *
from discord.ext import commands

class moderation(commands.GroupCog, name="moderation"):
    def __init__(self,bot = commands.Bot):
        self.bot = bot
    
    @commands.command(name="mod",description="Mods only")
    @commands.has_role("Mod")
    async def mod(self,ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Help pannel",description="Moderators Only",color=discord.Color.blurple())
            cursor = EmbedCursor(embed=embed)
            #Moderator help pannel
            cursor.add_row("Command","Syntax","Function",True)
            #add more moderator commands
            cursor.add_row("posts"," ","Get a list of post on the server, do !post help for more post commands")
            cursor.add_row("get-code"," ","Get COMET code on git repo, contact Vally for invite")
            cursor.add_row("db"," ","Get database size")
            
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="posts")
    @commands.has_role("Mod")
    async def posts(self,ctx):
        await ctx.message.delete()
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
        await ctx.message.delete()
        git_repo ="https://github.com/Needalife/Comet"
        embed = discord.Embed(title="Source code",description="This message will disapear after 10 seconds",color=discord.Color.dark_magenta(),url=f"{git_repo}")
        await ctx.send(embed=embed,delete_after=10.0)
        
    @commands.hybrid_command(name="kick")
    @commands.has_role("Mod")
    async def kick(self, ctx, user: discord.User, *, reason: str = "Not specified"):
        member = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = discord.Embed(description="User has administrator permissions.", color=0xE02B2B)
            await ctx.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    description=f"**{member}** was kicked by **{ctx.author}**!",
                    color=0xBEBEFE,
                )
                embed.add_field(name="Reason:", value=reason)
                await ctx.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{ctx.author}** from **{ctx.guild.name}**!\nReason: {reason}"
                    )
                except:
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B,
                )
                await ctx.send(embed=embed)
              
async def setup(bot:commands.Bot):
    await bot.add_cog(moderation(bot))