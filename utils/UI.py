import discord

class Choices(discord.ui.View):
    def __init__(self)->None:
        super().__init__()
        self.value = None
    
    @discord.ui.button(label="Yes",style=discord.ButtonStyle.blurple)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction)->None:
        self.value = "yes"
        self.stop() 
    
    @discord.ui.button(label="No", style=discord.ButtonStyle.blurple)
    async def cancel(self,button: discord.ui.Button, interaction: discord.Interaction)->None:
        self.value = "no"
        self.stop()