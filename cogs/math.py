from discord.ext import commands
from utils import Converter

class math(commands.Cog, name="math"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(name="cal",description="calulate equations")
    async def cal(self,ctx,expression: str):
        if not expression.strip():
            await ctx.send("Please enter an equation!")
            return
        
        try:
            job = Converter(expression)
            modified_expression = job.convert_operator()
            result = eval(modified_expression)
            
            await ctx.send(f"Result of {expression} is {result}")
        except Exception as e:
            await ctx.send(f"Error calculating equation {expression}, {e}")
        
async def setup(bot:commands.Bot):
    await bot.add_cog(math(bot))

