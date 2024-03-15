from discord.ext import commands
from utils.Mongo import *
from utils.Converter import *
from utils.EmbedCursor import *
from datetime import datetime
import discord

class storage(commands.Cog, name="storage"):
    def __init__(self, bot: commands.Bot) :
        self.bot = bot
    
    @commands.command(name="storage",description="store commands")
    async def storage(self,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Help pannel",description="store commands",color=discord.Color.blurple())
            cursor = EmbedCursor(embed=embed)

            cursor.add_row("Command","Syntax","Function",True)

            cursor.add_row("store","<link name> <link>","Store a link of your choice")
            cursor.add_row("links"," ","View the links you have store")
            cursor.add_row("del-link","<link name>","Delete link of your choice")
            
            await ctx.send(embed=embed)            
    
    @commands.hybrid_command(name="store",description="store important links")
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
        
        embed = discord.Embed(title=f"{user} links",color=discord.Color.green()).set_thumbnail(url=ctx.author.display_avatar)
        cursor = EmbedCursor(embed)
        
        cursor.add_row("Description","Link","Time added",True)
        
        for entry in data:
            current_time = datetime.strptime(entry['timestamp'],"%Y-%m-%d %H:%M:%S.%f%z")
            format_time = current_time.strftime("%B %d, %Y")
            cursor.add_row(f"{entry['title']}",f"{entry['link']}",f"{format_time}")

        await ctx.send(embed=embed)

    @commands.command(name="del-link",description="delete your saved link")
    async def del_personal_link(self,ctx,link_name):
        if ctx.message != 'all':
            user = ctx.author.name
            job = Mongo()
            job.delete_user_document('link','links',user,filter_is="title",filter_content=f"{link_name}")
            
            await ctx.send(f"Finish deleting {link_name}",delete_after=5.0)
    
    @commands.command(name="db")
    @commands.has_role("Mod")
    async def db(self,ctx):
        job = Mongo()
        embed = discord.Embed(title="Comet DB",color=discord.Color.green()).set_footer(text="Power by: MongoDB").set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2ZYtHv2OLXmthRPbkmENZRXuqBVDwlsrZ1A&usqp=CAU")
        final_size = 0
        
        for database in job.getAllDatabase():
            collections = job.getAllCollection(database)
            size_info = job.getSize(database=database, collections=collections)
            total_size = sum(size_info.values())
            final_size += total_size
            formatted_size_info = "\n".join([f"_{key}: {Converter.displayBytes(value)}" for key, value in size_info.items()])
            embed.add_field(name=f"{database}({Converter.displayBytes(total_size)})" , value=f"{formatted_size_info}", inline=False)
        
        embed.description = f"{Converter.displayBytes(final_size)} cluster"
        
        await ctx.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(storage(bot))