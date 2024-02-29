from discord.ext import commands

class math(commands.Cog, name="math"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(name="cal",description="calulate equations")
    async def cal(self,ctx,expression: str):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please enter an equation!")
        result = eval(expression)
        await ctx.send(f"Result of {expression} is {result}")
        
async def setup(bot:commands.Bot):
    await bot.add_cog(math(bot))