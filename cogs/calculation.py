from discord.ext import commands
from utils import Converter,EmbedCursor
from dotenv import load_dotenv
#do NOT remove math, its require for the eval() function
import discord,math,os,json,requests

load_dotenv()

def country_to_code(country):
    current_dir = os.path.dirname(__file__)
    currency_path = os.path.join(current_dir,'..','search_dict','currencies.json')
            
    with open(currency_path,'r',encoding='utf-8') as file:
        data = json.load(file)
    
    currency_name_to_code = {entry['country']: key for key,entry in data.items()}
    
    if country in currency_name_to_code:
        return currency_name_to_code[country]
    else:
        return None

class calculation(commands.Cog, name="math"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(name="cal",description="calulate equations")
    async def cal(self,ctx,*,expression: str):
        try:
            modified_expression = Converter(expression).final()
            result = eval(modified_expression)
            
            embed = discord.Embed(title="Calculator",description=f"{expression} = {result}",color=discord.Color.pink())
            
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f"Error calculating equation {expression}, {e}")
    
    @commands.group(name="convert",description="convert money, unit measurements")
    async def conversion(self,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Conversion Categories",color=discord.Color.dark_blue())
            cursor = EmbedCursor(embed=embed)
            cursor.add_row("Command","Syntax","Function",True)
            cursor.add_row("money","<amount of money> <country 1> <country 2>","Convert currency of country 1 to 2")
            cursor.add_row("unit","<unit 1> <unit 2>","Do unit conversion for unit 1 to 2")
            
            await ctx.send(embed=embed)

    @conversion.command(name="money")
    async def money(self,ctx,amount,code1,code2):
        
        if len(code1)>3:
            code1 = country_to_code(code1)
        
        if len(code2)>3:
            code2 = country_to_code(code2)
        
        exchange_rate_key = os.getenv('exchange_rate_api')
        url = f'https://v6.exchangerate-api.com/v6/{exchange_rate_key}/pair/{code1.upper()}/{code2.upper()}/{amount}'
        
        response = requests.get(url)
        data = response.json()

        rate = data["conversion_rate"]
        
        raw_result = data["conversion_result"]
        formatted_result = '{:,.2f}'.format(raw_result)
        formatted_amount = '{:,.2f}'.format(float(amount))
        
        raw_date = data["time_last_update_utc"]
        formatted_date = " ".join(raw_date.split(" ")[:4])
        
        embed = discord.Embed(title=f"{code1.upper()} -> {code2.upper()}",color=discord.Color.dark_purple()).set_footer(text=f"Power by: exchangerate-api.com").set_thumbnail(url="https://img.stackshare.io/stack/37303/657b34af1c7b9ea45750ae5720351d3735cf17d4.png")
        cursor = EmbedCursor(embed=embed)
        cursor.add_2_column_row("Conversion rate:",f"{rate}")
        cursor.add_2_column_row("Last update:", f"{formatted_date}")
        embed.add_field(name=f"**{formatted_amount} {code1.upper()}  =  {formatted_result} {code2.upper()}**",value="")
        
        await ctx.send(embed=embed)
    #to do
    @conversion.command(name="unit")
    async def unit(self,ctx):
        pass
    
async def setup(bot:commands.Bot):
    await bot.add_cog(calculation(bot))


