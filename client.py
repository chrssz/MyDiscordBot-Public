import discord
from discord.ext import commands
import wavelink

INTENTS = discord.Intents.all()
file_path = r'C:\Users\chris\Documents\Important\Discord\token.txt'

with open(file_path, "r") as token_file:
    TOKEN = token_file.read().strip()

cogslist = ['cogs.user_commands','cogs.economy','cogs.music']

class Client(commands.Bot):
    def __init__(self,commandprefix,intents = INTENTS):
        super().__init__(commandprefix, intents=INTENTS)
        
        @self.event 
        async def on_ready():
            print(f"Your bot, {self.user.name}, is now up!")
            await self.load_cogs()
            await self.sync_tree()
            await self.setup_wavelink()

    async def setup_wavelink(self):
        node: wavelink.node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self,nodes = [node])
        print(f"Wavelink connection has been connected")
        
    async def load_cogs(self):
        for element in cogslist:
            await self.load_extension(element)
            print(f"{element}, successfully loaded")
    
    async def sync_tree(self):
        synced = await self.tree.sync()
        print(f"{self.tree}, {str(len(synced))} commands synced")

    def initClient(self):
        self.run(TOKEN)
        