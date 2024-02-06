import os, discord, pandas as pd, re, requests
from dotenv import load_dotenv
from discord.ext import commands
from function import *

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
    match = re.match(r"(\d+)([+\-*/])(\d+)", expression)
    if match:
        x, operator, y = match.groups()
        job = Calculator(operator, int(x), int(y))
        result = job.calculation()
        await ctx.send(result)
    else:
        await ctx.send("Invalid input. Please provide the expression in the format: <number><operator><number>. (No space between operator and numbers)")
        await ctx.send("+: plus, -: minus, *: multiplication, /: division")

@bot.group()
async def gw2(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid function name. Please try something else.")

@gw2.command()
async def help(ctx):
    embed = discord.Embed(title="Help pannel",description="Syntax of all")
    await ctx.send(embed=embed)
        
@gw2.command(name="reg-api")
async def reg_api_key(ctx, name, key):
    def register_user_api(name,api_key):
        job = Mongo()
        job.write_user_api("gw2","api-key",name,api_key)
    
    register_user_api(name, key)
    await ctx.send(f"Finish registering {name} api key")

@gw2.command(name='del-api')
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

    data = get_user_info(name)
    account_name, account_time, account_fractal, account_wvw = data
    account_age = Calculator().display_time(account_time)
    
    if data:
        embed = discord.Embed(title=f"User: {account_name}")
        embed.add_field(name="Playtime:",value=f"{account_age}",inline=False)
        embed.add_field(name="Fractal level:",value=f"{account_fractal}",inline=False)
        embed.add_field(name="WvW rank:",value=f"{account_wvw}",inline=False)
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
    
    def to_embed(is_mystic,data):
        if is_mystic == True:
            output_item = data[0]['name']
            output_count = data[0]['output_item_count']

            mystic_embed = discord.Embed(title="Mystic Forge Recipe",description=f"{output_count} {output_item}")
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
            
            embed = discord.Embed(title="Recipe",description=f"{output_count} {output_item}")
            
            embed.add_field(name="Code:",value=f"{ingame_code}")
            embed.add_field(name=" ",value=" ")
            embed.add_field(name=" ",value=" ")
            embed.add_field(name="Disciplines:",value=f"{disciplines}")
            embed.add_field(name=" ",value=" ")
            embed.add_field(name=" ",value=" ")
            
            embed.add_field(name="Ingredient",value=" ")
            embed.add_field(name="Amount",value=" ")
            
            for i in data[0]["ingredients"]:
                item_id = i['item_id']
                item_name = get_name(item_id)
                item_count = i['count']
                embed.add_field(name=f"",value=f"{item_name}", inline=True)
                embed.add_field(name="",value=f"{item_count}", inline=True)
                embed.add_field(name="",value=f"", inline=True)
                
            return embed
        
    data = get_item_recipe(name)

    if len(data) == 2:
        
        mystic_forge_data, item_recipe_data = data
        
        await ctx.send(embed = to_embed(is_mystic=True,data=mystic_forge_data))
        await ctx.send(embed = to_embed(is_mystic=False,data=item_recipe_data))
    
bot.run(TOKEN)