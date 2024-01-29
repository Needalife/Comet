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
    print(f'🌠 {bot.user.name} has crashed on {GUILD} server!')

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

@bot.command()
async def gw2(ctx, function_name: str,name,key = None):
    
    def reg_api_key_function(name,api_key):
        job = Mongo()
        job.write("gw2","api-key",name,api_key)

    def del_api_function(name):
        job = Mongo()
        job.delete("gw2","api-key",name)
    
    def get_user_info(name):
        
        job = Mongo()
        
        try:
            data = job.read("gw2","api-key",name)
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
    
    def get_item_recipe(item_name):
        pass

    api_functions = {"reg-api": reg_api_key_function,"del-api": del_api_function}
    gw2_functions = {"get-stats": get_user_info,"get-recipe:": get_item_recipe}
    
    if function_name in api_functions:
        if key:
            api_functions[function_name](name = name, api_key = key)
            await ctx.send(f"Finish registering {name} api key")
        else:
            api_functions[function_name](name)
            await ctx.send(f"Finish deleting {name} api key")
            
    elif function_name in gw2_functions:
        if function_name == "get-stats":
            data = gw2_functions[function_name](name)
            account_name, account_time, account_fractal, account_wvw = data
            account_age = Calculator().display_time(account_time)
            
            if data:
                await ctx.send(f"User: {account_name}")
                await ctx.send(f"Play time: {account_age}")
                await ctx.send(f"Fractal level: {account_fractal}")
                await ctx.send(f"WvW level: {account_wvw}")
            else:
                await ctx.send("No data found, have you register your api yet?")
                
        elif function_name == "get-recipe":
            pass
    else:
        await ctx.send("Invalid function name. Please provide a valid function name.")
        
bot.run(TOKEN)