from discord.ext import commands
import discord,random

class Choice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None
    
    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "tails"
        self.stop()
    
class fun(commands.Cog, name="fun"):
    def __init__(self,bot: commands.Bot):
        self.bot = bot
    
    @commands.group(name="coin-flip",description="flip the coin :D")
    async def coin_flip(self,ctx) -> None:
        if ctx.invoked_subcommand is None:
            buttons = Choice()
            embed = discord.Embed(description="Heads or Tails?",color=0xBEBEFE)
            message = await ctx.send(embed=embed,view=buttons)
            await buttons.wait()
            
            result = random.choice(["heads","tails"])
            if buttons.value == result:
                embed = discord.Embed(
                    description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                    color=0xBEBEFE,
                )
            else:
                embed = discord.Embed(
                    description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                    color=0xE02B2B,
                )
            await message.edit(embed=embed, view=None, content=None)
    
    @coin_flip.command(name="pvp")
    async def cf_pvp(self, ctx):
        buttons = Choice()
        embed = discord.Embed(description="Pick Heads or Tails", color=0xBEBEFE)
        message = await ctx.send(embed=embed, view=buttons)
        
        await buttons.wait(60)
        user1 = ctx.author
        choice1 = "heads" if buttons.value == "heads" else "tails"
        
        await buttons.wait(60)
        user2 = ctx.author if buttons.value and ctx.author != user1 else None
        choice2 = "heads" if buttons.value == "heads" and user2 else "tails"
        
        if not user2:
            await ctx.send("Please wait for another player to make a choice, exit program.")
            return

        if choice1 == choice2:
            await ctx.send(f"{user2.display_name} picked the same side as {user1.display_name}")
        else:
            coin = random.choice(["heads", "tails"])
            await ctx.send(f"The coin landed on {coin}")
            
            if choice1 == coin:
                embed = discord.Embed(description=f"{user1.display_name} wins! 🪙")
                await message.edit(embed=embed, view = None, content=None)
            else:
                embed = discord.Embed(description=f"{user2.display_name} wins! 🪙")
                await message.edit(embed=embed, view = None, content=None)

async def setup(bot:commands.Bot):
    await bot.add_cog(fun(bot))