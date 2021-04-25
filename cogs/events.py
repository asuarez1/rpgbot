import discord
from discord.ext import commands
import db


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("==========================")
        print(f"{self.client.user.name} is online")
        print("==========================")
        # add all members bot can see to database
        for m in self.client.get_all_members():
            if m.id != self.client.user.id:
                member_id = str(m.id)
                member = await db.get_members(self.client.pg_con, member_id)
                if not member:
                    await db.add_member(self.client.pg_con, member_id)
                    print(f"added member: {member_id} to DB")

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        # add all members that join a guild the bot can see to database
        if ctx.id != self.client.user.id:
            member_id = str(ctx.id)
            member = await db.get_members(self.client.pg_con, member_id)
            if not member:
                await db.add_member(self.client.pg_con, member_id)
                print(f"added member: {member_id} to DB")


def setup(client):
    client.add_cog(Events(client))
