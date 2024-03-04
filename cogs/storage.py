from discord.ext import commands
from utils import *
from datetime import datetime
import discord

class storage(commands.Cog, name="storage"):
    def __init__(self, bot: commands.Bot) :
        self.bot = bot
    
    @commands.command(name="store",description="store important links")
    async def store(self,ctx,name: str,link: str):
        await ctx.message.delete()
        
        username = ctx.author.name
        job = Mongo(database='links')
        job.store_link(username,name,link)
        
        await ctx.send(f"Finish storing {name} into database",delete_after=10.0)
        
    @commands.hybrid_command(name="links",description="get links that you have store into the database")
    async def get_personal_link(self,ctx):
        
        user = ctx.author.name
        job = Mongo(database='links')
        data = job.get_links(user)
        
        embed = discord.Embed(title=f"{user} links",color=discord.Color.green())
        cursor = EmbedCursor(embed)
        
        cursor.add_row("Description","Link","Time added",True)
        for entry in data:
            current_time = datetime.strptime(entry['timestamp'],"%Y-%m-%d %H:%M:%S.%f%z")
            format_time = current_time.strftime("%B %d, %Y")
            cursor.add_row(f"{entry['title']}",f"{entry['link']}",f"{format_time}")
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="user-link",description="get user link, only mod can do this command")
    @commands.has_role("Mod")
    async def get_user_link(self,ctx):
        pass
    
async def setup(bot:commands.Bot):
    await bot.add_cog(storage(bot))