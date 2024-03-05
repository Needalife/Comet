from discord.ext import commands
from utils import Converter
#do NOT remove math, its require for the eval() function
import discord,math

class calculation(commands.Cog, name="math"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(name="cal",description="calulate equations")
    async def cal(self,ctx,*,expression: str):
        if not expression.strip():
            await ctx.send("Please enter an equation!")
            return
        
        try:
            modified_expression = Converter(expression).final()
            result = eval(modified_expression)
            
            embed = discord.Embed(title="Calculator",description=f"{expression} = {result}",color=discord.Color.pink())
            
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f"Error calculating equation {expression}, {e}")
    
async def setup(bot:commands.Bot):
    await bot.add_cog(calculation(bot))


