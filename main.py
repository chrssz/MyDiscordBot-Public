
from discord.ext import commands
from client import Client
def main():
    client = Client(commandprefix='!')
    client.initClient()

if __name__ == "__main__":
    main()
