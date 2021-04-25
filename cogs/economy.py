import discord
from discord.ext import commands
import db


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gold(self, ctx):
        member_id = str(ctx.author.id)
        member = await db.get_member_class(self.client.pg_con, member_id)
        await ctx.send(f"You have {member.gold} gold.")


def setup(client):
    client.add_cog(Economy(client))
