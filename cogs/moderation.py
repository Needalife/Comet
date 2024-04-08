import discord
from utils.EmbedCursor import *
from discord.ext import commands
from models.User import *
from utils.Mongo import *
from utils.UI import *
           
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
            cursor.add_row("del-post","<post>","Delete a post")
            cursor.add_row("source-code"," ","Get COMET code on git repo, contact Vally for invite")
            cursor.add_row("db"," ","Get database stats")
            cursor.add_row("track","<name> <reason>","track a user, reason can be optional, if no name is specified, retrieve all tracks user")
            
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

    @commands.hybrid_command(name="del-post")
    @commands.has_role("Mod")
    async def del_post(self,ctx,*,post:str):
        await ctx.message.delete()
        guild = ctx.guild
        threads = guild.threads

        for thread in threads:
            if thread.name.upper() == post.upper():
                await thread.delete()
                await ctx.send(f"Successfully deleting post: {thread.name}",delete_after=10.0)
                break
            else:
                await ctx.send(f"No post name: {post}",delete_after=10.0)
                break

    @commands.hybrid_command(name="source-code")
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
    
    @commands.hybrid_command(name="track")
    @commands.has_role("Mod")
    async def track(self,ctx,user: discord.User = None, *, reason: str = "Not specified"):
        
        if user is None:
            embed = discord.Embed(title="Track Users",description="User that has been track",color=discord.Color.dark_gray())
            
            cursor = EmbedCursor(embed)
            cursor.add_row('Name','Reason','Date Created',True)
            
            user_data = [{'name':user['name'],'reason':user['description'],'created_at':user['created_at']} for user in track().getTrackUser()]
            for user in user_data:
                cursor.add_row(user['name'],user['reason'],user['created_at'])
            
            await ctx.send(embed=embed)
        else:    
            try:
                user_data = User(
                            user.display_name,
                            user.created_at.strftime("%d/%m/%Y"),
                            user.id,
                            user.display_avatar,
                            reason
                            ).data("json")
                
                track(user_data)
                
            except Exception as e:
                print(f"Error: {e}")
            
            embed = discord.Embed(title=f"Track user {user.display_name}",description=f"Reason: {reason}",color=discord.Color.brand_red())
            embed.set_thumbnail(url=f"{user.display_avatar}")
            
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="clear-track")
    @commands.has_role("Mod")
    async def clear_track(self,ctx,user: discord.User) -> None:
        buttons = Choices()
        embed = discord.Embed(title=f"You sure want to stop tracking {user.display_name}?")
        message =  await ctx.send(embed=embed,view=buttons)
        await buttons.wait()
        
        if buttons.value == 'yes':
            embed = discord.Embed(description=f"Stop tracking user {user.display_name}")
            job = track()
            job.deleteUser(user.id)
        else:
            embed = discord.Embed(description=f"Cancel command !clear-track {user.display_name}")
            
        await message.edit(embed=embed,view=None,content=None)
        
    @commands.hybrid_command(name="reg-all")
    @commands.has_role("Mod")
    async def reg_all(self,ctx):
        pass
    
async def setup(bot:commands.Bot):
    await bot.add_cog(moderation(bot))

