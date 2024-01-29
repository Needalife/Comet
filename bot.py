import os, discord, pandas as pd, re
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
        
    api_functions = {"reg-api": reg_api_key_function,"del-api": del_api_function}
    
    if function_name in api_functions:
        if key:
            api_functions[function_name](name = name, api_key = key)
            await ctx.send(f"Finish registering {name} api key")
        else:
            api_functions[function_name](name)
            await ctx.send(f"Finish deleting {name} api key")
    
    else:
        await ctx.send("Invalid function name. Please provide a valid function name.")

bot.run(TOKEN)