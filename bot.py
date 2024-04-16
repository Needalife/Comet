import os, discord,asyncio
from dotenv import load_dotenv
from discord.ext import commands
from utils.Mongo import track
from utils.Converter import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
        self.user_data = None
        self.track_channel_id = os.getenv('track_log_channel_id')
        
    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    print(f"Loaded extension {extension}✅")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}❌")
                    
    async def setup_hook(self):
        await self.load_cogs()
        print(f'discord.py API version: {discord.__version__}')
    
    async def fetch_user_data(self):
        self.user_data = [user['name'][0] for user in track().getTrackUser()]
    
    async def periodic_update(self,interval_minutes):
        while True:
            await self.fetch_user_data()
            await asyncio.sleep(interval_minutes * 60)
    
    async def on_ready(self):
        print(f'🌠 {self.user.name} has crashes on {GUILD} server!')
        if self.track_channel_id:
            await self.periodic_update(1)
    
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        await bot.process_commands(message)
        
        if message.author.name in self.user_data:
            track_channel = self.get_channel(int(self.track_channel_id))
            current_time = Converter().timeVN(datetime.now())
            await track_channel.send(f"[{current_time}]{message.channel.mention} {message.author.display_name}: {message.content}")
            
    async def on_member_join(self,member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to {GUILD}!')
    
if os.path.exists(path=f".env"):
    print(f'Reading .env file...')
    bot = Bot()
    bot.run(TOKEN)
else:
    print("No .env file found, proceed to exit the program")