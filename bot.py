import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncpg


load_dotenv()
TOKEN = os.getenv('TOKEN')
DB_PASS = os.getenv('DB_PASS')
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=">", intents=intents)


async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(database="devbot", user="postgres", password=DB_PASS)
    print(f"established connection to DB")


def load_cogs():
    for cog in os.listdir(".\\cogs"):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                client.load_extension(cog)
                print(f"{cog} was loaded")
            except Exception as e:
                print(f"{cog} cannot be loaded:")
                raise e


print("connecting to DB")
client.loop.run_until_complete(create_db_pool())
print("loading cogs")
load_cogs()
client.run(TOKEN)
