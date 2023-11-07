import discord
from discord.ext import commands
from discord import app_commands
import random
import csv

##declaraton of user commands, and normal commands
class Commands(commands.Cog, name = 'General Commands'):
    @app_commands.command(name = "hello", description ="Says hello")
    async def hello(self,interaction: discord.Interaction):
        await interaction.response.send_message("Just a test")
    @app_commands.command(name = "inspire", description ="Generates a random inspiration quote")
    async def inspire(self,interaction: discord.Interaction):
        with open("quote.csv", "r", newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            random_line_number = random.randint(1, 1000)
            csvfile.seek(0)
            for line_number,row in enumerate(csv_reader,start =1):
                    if line_number == random_line_number:
                        author, quote = row
                        author = author.strip('""')
                        quote = quote.strip('""')
                        await interaction.response.send_message(f"\n - Inspirational Quote: ***{quote}*** By: ***{author}***")
                        break
     


async def setup(bot):
    await bot.add_cog(Commands(bot))