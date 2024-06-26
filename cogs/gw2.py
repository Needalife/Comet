import discord,requests,os,json,pytz
from utils.Mongo import *
from utils.EmbedCursor import *
from utils.Converter import *
from discord.ext import commands
from datetime import datetime, timedelta
from datetimerange import DateTimeRange

def splitTimeRange(time_range:str,delimeter:str):
    start_time, end_time = time_range.split(delimeter)
    return start_time.strip(),end_time.strip()
    
def getKournaFishingCycle() -> list:
    current_dir = os.path.dirname(__file__)
    gw2cycle_path = os.path.join(current_dir, '..', 'search_dict', 'gw2Time.json')

    with open(gw2cycle_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Function to parse time strings into datetime objects
    def parse_time(time_str):
        return datetime.strptime(time_str, "%H:%M")
    
    day_cycle = []
    for state in data['Tyria']:
        if state['stage'] == 'Day':
            start_time = parse_time(state['start'])
            end_time = parse_time(state['end'])
            day_cycle.append((start_time, end_time))
    # Sort the time ranges based on their start times
    sorted_day_cycle = sorted(day_cycle, key=lambda x: x[0])
    # Convert sorted time ranges back to string representation
    sorted_day_cycle_strings = [f"{start.strftime('%H:%M')} ~ {end.strftime('%H:%M')}" for start, end in sorted_day_cycle]

    return sorted_day_cycle_strings
        
def getItemName(item_id):
    job = gw2Items("gw2_items")
    return job.get_item_name(item_id)

def getItemRecipe(name):
    job = gw2Items("gw2_items")
    return job.get_item_recipe(name)       

def getIcon(item_name):
    job = gw2Items("gw2_items")
    return job.get_item_icon(item_name)

def getEvents(expansion) -> list:
    current_dir = os.path.dirname(__file__)
    gw2_event_cycle_path = os.path.join(current_dir,'..','search_dict','gw2Event.json')

    with open(gw2_event_cycle_path,'r',encoding='utf-8') as file:
        data = json.load(file)
    
    return [({'name': f"{event['name']}",
                'first': f"{event['first']}",
                'last': f"{event['last']}",
                'interval': f"{event['interval']}",
                'duration' : f"{event['duration']}",
                'location' : f"{event['location']}"}) for event in data[f'{expansion}']]

def checkOngoing(avail_time: list, current_time, duration: int):
    next_event_time = None
    for time in avail_time:
        time = time.replace(tzinfo=current_time.tzinfo)
        if time > current_time:
            next_event_time = time
            break
    
    if next_event_time:
        time_difference = (next_event_time.timestamp() - current_time.timestamp()) / 60
        if time_difference <= duration and current_time > time:
            return True
        else:
            return int(time_difference)
        
class gw2(commands.GroupCog, name="gw2"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="gw2",description="GW2 commands")
    async def gw2(self,ctx):
        if ctx.invoked_subcommand is None:
            embed1 = discord.Embed(title="Help pannel",description="GW2 commands",color=discord.Color.red())
            cursor1 = EmbedCursor(embed=embed1)
            #GW2 help pannel
            cursor1.add_row("Command","Syntax","Function",True)
            cursor1.add_row("reg-api","<name of your choice> <your gw2 api>","Register your gw2 api to a name of your choice")
            cursor1.add_row("del-api","<name of your registered api>","Delete your registered api")
            cursor1.add_row("get-stats","<name of your registered api>","Get ingame user stat")
            cursor1.add_row("recipe","<item name>","Get recipe or mystic forge recipe or both")
            cursor1.add_row("price","<item name>","Get trading post price")
            cursor1.add_row("ET","<expansion>","Show event timer for expansion of choices")
            
            embed2 = discord.Embed(title="Help pannel",description=" ",color=discord.Color.red())
            cursor2 = EmbedCursor(embed=embed2)
            cursor2.add_row("clover"," ","Mystic Clover WvW one time reward track :D")
            cursor2.add_row("fish"," ","Show the fishing time of Kourna")
            
            await ctx.send(embed=embed1)
            await ctx.send(embed=embed2)

    @gw2.command(name="reg-api")
    async def reg_api_key(self, ctx, name, key):
        try:
            job = gw2Items("api-key")
            job.write_user_api(name,key)
            await ctx.send(f"Finish registering {name} api key")
            await ctx.message.delete()
            
        except Exception:
            await ctx.send(f"{Exception}")
        
    @gw2.command(name='del-api')
    @commands.has_role("Mod")
    async def del_api_key(self,ctx, user_name):
        job = gw2Items("api-key")
        job.delete_user_api(user_name)
        
        await ctx.send(f"Finish deleting user {user_name} api key")
        await ctx.message.delete()
    
    @gw2.command(name="get-stats")
    async def get_stats(self,ctx,name):
        
        job = gw2Items("api-key")
        data = job.get_user_info(name)
        account_name, account_time, account_fractal, account_wvw = data
        account_age = Converter().displayTime(account_time)
        leg_data = job.get_user_leggy()
        
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
                    
                    #update obsidian armor into database ffs (todo)
                    try:
                        leg_name = getItemName(f"{leg_data}")
                    except Exception:
                        leg_name = "Item_to_be_added"
                        
                    leg_list.append(leg_name)
                
                cursor.add_2_column_row("Legendaries:",f"{leg_list}")
        
            await ctx.send(embed=embed)
        else:
            await ctx.send("No data found, have you register your api yet?")
            
    @gw2.command()
    async def recipe(self, ctx, *, name: str):        
        def to_embed(is_mystic,data):
            if is_mystic == True:
                output_item = data[0]['name']
                output_count = data[0]['output_item_count']

                mystic_embed = discord.Embed(title="Mystic Forge Recipe",description=f"{output_count} {output_item}",color=discord.Color.blue())
                mystic_embed.set_thumbnail(url=f"{getIcon(output_item)}")
                
                mystic_embed.add_field(name="Ingredient",value=" ")
                mystic_embed.add_field(name="Amount",value=" ")
                mystic_embed.add_field(name=" ",value=" ")
                
                for i in data[0]['ingredients']:
                    item_id = i['id']
                    item_name = getItemName(item_id)
                    item_count = i['count']
                    mystic_embed.add_field(name=f"",value=f"{item_name}", inline=True)
                    mystic_embed.add_field(name="",value=f"{item_count}", inline=True)
                    mystic_embed.add_field(name="",value=f"", inline=True)
                
                return mystic_embed
            else:
                output_item_id = data[0]["output_item_id"]
                output_item = getItemName(output_item_id)
                output_count = data[0]["output_item_count"]
                ingame_code = data[0]["chat_link"]
                disciplines = data[0]["disciplines"]
                
                embed = discord.Embed(title="Recipe",description=f"{output_count} {output_item}",color=discord.Color.dark_orange())
                embed.set_thumbnail(url=f"{getIcon(output_item)}")
                
                embed.add_field(name="Ingredient",value=" ")
                embed.add_field(name="Amount",value=" ")
                embed.add_field(name=" ",value=" ")
                
                for i in data[0]["ingredients"]:
                    item_id = i['item_id']
                    item_name = getItemName(item_id)
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
            
        data = getItemRecipe(name)

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
    async def price(self,ctx, *, item_name: str):
        job = gw2Items("gw2_items")
        
        api_endpoint = f"https://api.guildwars2.com/v2/commerce/prices/{job.get_item_id(item_name)}"
        response = requests.get(api_endpoint)
        data = response.json()
        
        buys = data['buys']
        sells = data['sells']
        
        embed = discord.Embed(title=f"{item_name}",color=discord.Color.gold())
        embed.set_thumbnail(url=f"{getIcon(item_name)}")
        cursor = EmbedCursor(embed=embed)
                                
        gold, silver, copper = Converter().displayCurrency(buys['unit_price'])
        cursor.add_row("Buy Order"," "," ",True)
        cursor.add_2_column_row("Highest buy order:",f"{gold} gold, {silver} silver, {copper} copper")
        cursor.add_2_column_row("Total buy orders:",f"{buys['quantity']}")
        
        gold, silver, copper = Converter().displayCurrency(sells['unit_price'])
        cursor.add_row("Sell Order"," "," ",True)
        cursor.add_2_column_row("Lowest sell order:",f"{gold} gold, {silver} silver, {copper} copper")
        cursor.add_2_column_row("Total sell orders:",f"{sells['quantity']}")
        
        await ctx.send(embed=embed)

    @gw2.command(name="clover")
    async def mystic_clover(self,ctx):
        embed1 = discord.Embed(title="Mystic Clover",description="None repeatable,one time,no reqs",color=discord.Color.green())
        cursor1 = EmbedCursor(embed=embed1)
        cursor1.add_row("Track","","Amount",True)
        cursor1.add_row("Warclaw Reward Track","","7🍀")
        cursor1.add_row("Silverwastes Reward Track","","7🍀")
        cursor1.add_row("Verdant Brink Reward Track","","7🍀")
        cursor1.add_row("Grothmar Valley Reward Track","","9🍀")
        await ctx.send(embed=embed1)
        
        embed2 = discord.Embed(title="Mystic Clover",description="None repeatable,one time,have reqs",color=discord.Color.green())
        cursor2 = EmbedCursor(embed=embed2)
        cursor2.add_row("Track","","Amount",True)
        cursor2.add_row("Shiver Emote Tome Reward Track","","6🍀")
        cursor2.add_row("Auric Basin Reward Track","","7🍀")
        cursor2.add_row("Tangled Depths Reward Track","","7🍀")
        cursor2.add_row("Bjora Marches Reward Track","","11🍀")
        cursor2.add_row("Drizzle Coast Reward Track","","14🍀")
        await ctx.send(embed=embed2)
        
        embed3 = discord.Embed(title="Mystic Clover",description="First completion",color=discord.Color.green())
        cursor3 = EmbedCursor(embed=embed3)
        cursor3.add_row("Track","","Amount",True)
        cursor3.add_row("Crystal Desert Reward Track","","7🍀")
        cursor3.add_row("End of Dragons Reward Track","","7🍀")
        cursor3.add_row("Long-Lost Tahkayun Weapons Reward Track","","7🍀")
        cursor3.add_row("Xunlai Customer Loyalty Perks Program","","7🍀")
        await ctx.send(embed=embed3)
    
    @gw2.command(name='fish')
    async def gw2_fishing(self,ctx):
        await ctx.message.delete()
        
        available_time = getKournaFishingCycle()
        current_time = Converter().timeVN(datetime.now(),is12HourFormat=True) #string
        
        embed = discord.Embed(title="Kourna Fishing Timetable",description="VN time",color=discord.Color.gold())
        cursor = EmbedCursor(embed)
        cursor.add_row("Time","Active?","Upcoming",isHeader=True)
        #Shit is ugly, I know :') - Vally
        for time_range in available_time:
            start_time, end_time = splitTimeRange(time_range,'~')
            if current_time in DateTimeRange(start_time,end_time): #Condition for current time in range of avail time
                cursor.add_row(f"{time_range}","✅","❌")
                continue
            elif int(current_time.split(":")[0]) == 12 and 39 < int(current_time.split(":")[1]) <= 59 and start_time == '1:30':
                minutes_left = 30 + (60-int(current_time.split(":")[1]))
                cursor.add_row(f"{time_range}","❌",f"in {minutes_left} minutes")
                continue
            elif 0 <= int(start_time.split(":")[0]) - int(current_time.split(":")[0]) < 2: #Catch closest avail time
                if int(start_time.split(":")[0]) == int(current_time.split(":")[0]):
                    minutes_left = int(start_time.split(":")[1]) - int(current_time.split(":")[1])
                    cursor.add_row(f"{time_range}","❌",f"in {minutes_left} minutes")
                    continue
                cursor.add_row(f"{time_range}","❌","✅")
            else:
                cursor.add_row(f"{time_range}","❌","❌")
        
        await ctx.send(embed=embed,delete_after=900.0)
    
    @gw2.command()
    async def ET(self,ctx, *, expansion: str):
        await ctx.message.delete()
        
        embed = discord.Embed(title="Events Timer",description=f"{expansion}",color=discord.Color.random())
        cursor = EmbedCursor(embed)    
        cursor.add_row("Event","Status","Waypoint",True)
        
        vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.now(tz=vietnam_timezone)
        for event in getEvents(expansion.upper()):
            start_time = datetime.combine(datetime.now().date(),datetime.strptime(event['first'], "%H:%M").time())
            end_time = datetime.combine(datetime.now().date(),datetime.strptime(event['last'], "%H:%M").time())
            event_duration = int(event['duration'])
            available_time = []
            
            while start_time <= end_time:
                available_time.append(start_time)
                start_time = start_time + timedelta(hours=int(event['interval']))
            
            isAvailable = checkOngoing(avail_time=available_time,current_time=current_time,duration=event_duration)
            
            if isAvailable is True:
                cursor.add_row(f"{event['name']}","ongoing",f"{event['location']}")
            else:
                cursor.add_row(f"{event['name']}",f"start in {isAvailable} minutes",f"{event['location']}")
        
        await ctx.send(embed=embed,delete_after=60.0)

async def setup(bot:commands.Bot):
    await bot.add_cog(gw2(bot))