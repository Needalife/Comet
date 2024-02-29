from discord.ext import commands

class cal(commands.Cog, name="cal"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(name="cal",description="calulate equations")
    async def cal(self,ctx,expression: str):
        result = eval(expression)
        await ctx.send(f"Result of {expression} is {result}")
        
async def setup(bot:commands.Bot):
    await bot.add_cog(cal(bot))