import os, discord,requests
from dotenv import load_dotenv
from discord.ext import commands
from utils import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
    
    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    print(f"Loaded extension {extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")
                    
    async def setup_hook(self):
        await self.load_cogs()
        print(f'discord.py API version: {discord.__version__}')
        print(f'🌠 {self.user.name} has crashes on {GUILD} server!')
        
    async def on_member_join(self,member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to {GUILD}!')

    async def on_message(self,message):
        if message == '!get-code':
            await message.delete(10)
            
bot = Bot()
    
bot.run(TOKEN)