import os, discord,requests
from dotenv import load_dotenv
from discord.ext import commands
from utils import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

try:
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!',intents=intents);
except Exception as e:
    print(e)
    
@bot.event
async def on_ready():
    print(f'🌠 {bot.user.name} has crashes on {GUILD} server!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {GUILD}!'
    )

@bot.command(name="cal",help="calculator for basic calculations")
async def calculation(ctx, expression: str):
    result = eval(expression)
    await ctx.send(f"Result of {expression} is {result}")
#gw2 stuff...
@bot.group()
async def gw2(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid function name. Please try something else.")

@gw2.command()
async def help(ctx):
    embed = discord.Embed(title="Help pannel",description="GW2 commands",color=discord.Color.red())
    cursor = EmbedCursor(embed=embed)
    #GW2 help pannel
    cursor.add_row("Command","Syntax","Function",True)
    cursor.add_row("help"," ","Display this message")
    cursor.add_row("reg-api","<name of your choice> <your gw2 api>","Register your gw2 api to a name of your choice")
    cursor.add_row("del-api","<name of your registered api>","Delete your registered api")
    cursor.add_row("get-stats","<name of your registered api>","Get ingame user stat")
    cursor.add_row("recipe","<item name>","Get recipe or mystic forge recipe or both")
    cursor.add_row("price","<item name>","Get trading post price")
    
    await ctx.send(embed=embed)
        
@gw2.command(name="reg-api")
async def reg_api_key(ctx, name, key):
    def register_user_api(name,api_key):
        job = Mongo()
        job.write_user_api("gw2","api-key",name,api_key)
    
    register_user_api(name, key)
    await ctx.send(f"Finish registering {name} api key")

@gw2.command(name='del-api')
@commands.has_role("Mod")
async def del_api_key(ctx, user_name):
    def delete_user_api(name):
        job = Mongo()
        job.delete_user_api("gw2","api-key",name)
    
    delete_user_api(user_name)
    await ctx.send(f"Finish deleting {user_name} api key")
    
@gw2.command(name="get-stats")
async def get_stats(ctx,name):
    def get_user_info(name):
        
        job = Mongo()
        
        try:
            data = job.read_user_api("gw2","api-key",name)
            for value in data: key = value['key']
            gw2_url = 'https://api.guildwars2.com/v2/account'
            headers = {'Authorization': f'Bearer {key}'}
            response = requests.get(gw2_url, headers=headers)
            
            if response.status_code == 200:
                account_data = response.json()
                return account_data['name'],account_data['age'],account_data['fractal_level'],account_data['wvw_rank']
            else:
                return None
        except:
            return None
    
    def get_user_leggy(name):
        job = Mongo()
        
        data = job.read_user_api("gw2","api-key",name)
        for value in data: key = value['key']
        
        leggy_url = 'https://api.guildwars2.com/v2/account/legendaryarmory'
        headers = {'Authorization': f'Bearer {key}'}
        response = requests.get(leggy_url, headers=headers)
        
        leggys_data = response.json()
        
        return leggys_data
    
    def get_item_name(item_id):
        job = Mongo()
        
        return job.get_item_name("gw2_items",f"{item_id}")

    data = get_user_info(name)
    account_name, account_time, account_fractal, account_wvw = data
    account_age = Calculator().display_time(account_time)
    leg_data = get_user_leggy(name)
    
    if data:
        embed = discord.Embed(title=f"User: {account_name}",color=discord.Color.green())
        cursor = EmbedCursor(embed)
        cursor.add_2_column_row("Playtime:",f"{account_age}")
        cursor.add_2_column_row("Fractal level:",f"{account_fractal}")
        cursor.add_2_column_row("WvW rank:",f"{account_wvw}")
        
        if leg_data:
            
            leg_list = []

            for i in leg_data:
                leg_data = i['id']
                leg_name = get_item_name(f"{leg_data}")
                leg_list.append(leg_name)
            
            cursor.add_2_column_row("Legendaries:",f"{leg_list}")
    
        await ctx.send(embed=embed)
    else:
        await ctx.send("No data found, have you register your api yet?")
    
@gw2.command()
async def recipe(ctx, *, name: str):
    def get_item_recipe(name):
        job = Mongo()
        return job.get_recipe('gw2_items',name)
    
    def get_name(item_id):
        job = Mongo()
        return job.get_item_name("gw2_items",item_id)
    
    def get_icon(item_name):
        job = Mongo()
        return job.get_item_icon(item_name)
    
    def to_embed(is_mystic,data):
        if is_mystic == True:
            output_item = data[0]['name']
            output_count = data[0]['output_item_count']

            mystic_embed = discord.Embed(title="Mystic Forge Recipe",description=f"{output_count} {output_item}",color=discord.Color.blue())
            mystic_embed.set_thumbnail(url=f"{get_icon(output_item)}")
            
            mystic_embed.add_field(name="Ingredient",value=" ")
            mystic_embed.add_field(name="Amount",value=" ")
            mystic_embed.add_field(name=" ",value=" ")
            
            for i in data[0]['ingredients']:
                item_id = i['id']
                item_name = get_name(item_id)
                item_count = i['count']
                mystic_embed.add_field(name=f"",value=f"{item_name}", inline=True)
                mystic_embed.add_field(name="",value=f"{item_count}", inline=True)
                mystic_embed.add_field(name="",value=f"", inline=True)
            
            return mystic_embed
        else:
            output_item_id = data[0]["output_item_id"]
            output_item = get_name(output_item_id)
            output_count = data[0]["output_item_count"]
            ingame_code = data[0]["chat_link"]
            disciplines = data[0]["disciplines"]
            
            embed = discord.Embed(title="Recipe",description=f"{output_count} {output_item}",color=discord.Color.dark_orange())
            embed.set_thumbnail(url=f"{get_icon(output_item)}")
            
            embed.add_field(name="Ingredient",value=" ")
            embed.add_field(name="Amount",value=" ")
            embed.add_field(name=" ",value=" ")
            
            for i in data[0]["ingredients"]:
                item_id = i['item_id']
                item_name = get_name(item_id)
                item_count = i['count']
                embed.add_field(name=f"",value=f"{item_name}", inline=True)
                embed.add_field(name="",value=f"{item_count}", inline=True)
                embed.add_field(name="",value=f"", inline=True)
            
            embed.add_field(name="Code:",value=f"", inline=True)
            embed.add_field(name=f"",value=f"{ingame_code}", inline=True)
            embed.add_field(name="",value=f"", inline=True)
            
            embed.add_field(name="Disciplines:",value=f"", inline=True)
            embed.add_field(name=f"",value=f"{disciplines}", inline=True)
            embed.add_field(name="",value=f"", inline=True)
            
            return embed
        
    data = get_item_recipe(name)

    if data is None:
        await ctx.send("No recipe found :(")
    else:
        mystic_forge_data, item_recipe_data = data
        if not item_recipe_data:
            await ctx.send(embed = to_embed(is_mystic=True,data=mystic_forge_data))
        elif not mystic_forge_data:
            await ctx.send(embed = to_embed(is_mystic=False,data=item_recipe_data))
        else:
            await ctx.send(embed = to_embed(is_mystic=True,data=mystic_forge_data))
            await ctx.send(embed = to_embed(is_mystic=False,data=item_recipe_data))

@gw2.command()
async def price(ctx, *, item_name: str):
    def get_id(item_name):
        job = Mongo()
        return job.get_item_id("gw2_items",item_name)
    
    def get_icon(item_name):
        job = Mongo()
        return job.get_item_icon(item_name)
    
    def get_currency(copper):
        job = Calculator()
        return job.display_currency(copper)
    
    api_endpoint = f"https://api.guildwars2.com/v2/commerce/prices/{get_id(item_name)}"
    response = requests.get(api_endpoint)
    data = response.json()
    
    buys = data['buys']
    sells = data['sells']
    
    embed = discord.Embed(title=f"{item_name}",color=discord.Color.gold())
    embed.set_thumbnail(url=f"{get_icon(item_name)}")
    cursor = EmbedCursor(embed=embed)
    
    gold, silver, copper = get_currency(buys['unit_price'])
    cursor.add_row("Buy Order"," "," ",True)
    cursor.add_2_column_row("Highest buy order:",f"{gold} gold, {silver} silver, {copper} copper")
    cursor.add_2_column_row("Total buy orders:",f"{buys['quantity']}")
    
    gold, silver, copper = get_currency(sells['unit_price'])
    cursor.add_row("Sell Order"," "," ",True)
    cursor.add_2_column_row("Lowest sell order:",f"{gold} gold, {silver} silver, {copper} copper")
    cursor.add_2_column_row("Total sell orders:",f"{sells['quantity']}")
    
    await ctx.send(embed=embed)
    
@gw2.command()
async def masteries (ctx):
    return
#Moderation stuff...
@bot.group()
@commands.has_role("Mod")
async def mod(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid function name, do !mod help.")
        
@mod.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Help pannel",description="Moderators Only",color=discord.Color.blurple())
    cursor = EmbedCursor(embed=embed)
    #Moderator help pannel
    cursor.add_row("Command","Syntax","Function",True)
    cursor.add_row("help"," ","Display this message")
    #add more moderator commands
    cursor.add_row("posts"," ","Get a list of post on the server, do !post help for more post commands")
    cursor.add_row("get-code"," ","Get COMET code on git repo, contact Vally for invite")
    
    await ctx.send(embed=embed)

@mod.command(name="get-code")
async def get_comet_github_link(ctx):
    await ctx.send("https://github.com/Needalife/Comet")
    
@mod.command(name="posts")
async def posts(ctx):
    guild = ctx.guild
    threads = guild.threads
    
    embed = discord.Embed(title="Post list",color=discord.Color.purple())
    cursor = EmbedCursor(embed=embed)
    
    cursor.add_row("Post","OP's","Forum")
    for thread in threads:
        user = await bot.fetch_user(thread.owner_id)
        cursor.add_row(thread.jump_url,user.mention,thread.parent)
    
    await ctx.send(embed=embed)
    
@bot.group()
async def post(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid post function, do !post help.")

@post.command()
async def help(ctx):
    embed = discord.Embed(title="Help pannel",description="Post commands",color=discord.Color.blurple())
    cursor = EmbedCursor(embed=embed)
    cursor.add_row("Command","Syntax","Function",True)
    cursor.add_row("help"," ","Display this message")
    #Post commands
    
    await ctx.send(embed=embed)
    
bot.run(TOKEN)