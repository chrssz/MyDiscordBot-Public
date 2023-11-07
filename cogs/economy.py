import discord
from discord.ext import commands
from discord.ext.commands import is_owner
import random
import json
import asyncio
class IntConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return int(argument)
        except ValueError:
            await ctx.send("**Error not an Integer**")
            raise commands.BadArgument("Invalid integer amount")

class Economy(commands.Cog, name='Economy'):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.json_filename = 'userdata.json'
        self.load_data()
    def load_data(self):
        try:
            with open(self.json_filename, 'r') as json_file:
                self.data = json.load(json_file)
                print(f"{self.data} data loaded")
        except FileNotFoundError:
            self.data = {}
            print(f"Error loading {self.data} data")
    def save_data(self):
        with open(self.json_filename, 'w') as json_file:
            json.dump(self.data, json_file)
            print(f"Saved data: {self.data}")
    def check_data(self,user_id): #check for data if present
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id]= {'wallet': 200} #init data
        return self.data[user_id]
    def add_to_wallet(self,user_id,amount):
        user_data = self.check_data(user_id)
        user_data['wallet'] += amount
        print(f"Added {amount}, to {user_id}.")
        self.save_data()
    def minus_from_wallet(self,user_id, amount):
        user_data = self.check_data(user_id)
        user_data['wallet'] -= amount
        print(f"Subtracted {amount}, to {user_id}.")
        self.save_data()
    #games
    @commands.command()
    async def flipcoin(self,ctx,amount:IntConverter, choice: str): #!flipcoin int choice
        user_choice = choice.lower()
        user_data = self.check_data(ctx.author.id)
        user_wallet = user_data['wallet']
        if amount > 0:
            if user_wallet < amount:
                await ctx.send(f"***-Error: You do not have the funds for this bet***")
            else:
                if user_choice not in ["heads", "tails"]:
                    await ctx.send("***Error: Please choose 'heads' or 'tails'")
                else:
                    winner = random.choice(["heads","tails"])
                    if user_choice == winner:
                        await ctx.send(f"***You win {amount}!!!***")
                        self.add_to_wallet(ctx.author.id,amount)
                    else:
                        self.minus_from_wallet(ctx.author.id,amount)
                        await ctx.send(f"*** You lose {amount}***")
        else:
            await ctx.send(f"***-Error: Cannot place negative bets***")
    
    
    #balance / user related commands
    @commands.command(hidden=True)
    @is_owner()
    async def addbal(self,ctx, amount: IntConverter):
        user_data = self.add_to_wallet(ctx.author.id, amount)
        if amount >= 0:
            await ctx.send(f"***Successfully added {amount} to your wallet!***")
        else:
            await ctx.send(f"***Successfully subtracted {-1* amount} from your wallet!***")
    @commands.command()
    async def bal(self,ctx):
        user_data = self.check_data(ctx.author.id)
        user_wallet = user_data['wallet']
        await ctx.send(f"***Your balance is: {user_wallet}***")
    
        
    


async def setup(bot):
    await bot.add_cog(Economy(bot))