from combat import buffs
from discord.ext import commands
import db


class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        try:
            self.client.unload_extension(f"cogs.{cog}")
            self.client.load_extension(f"cogs.{cog}")
            print(f"Cog {cog} was reloaded.")
            await ctx.send(f"Cog {cog} was reloaded.")
        except Exception as e:
            print(f"Cog {cog} failed to reload:")
            raise e

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        xp = 0
        for i in range(0, 50):
            if i == 0:
                xp = 100
            else:
                xp += (xp / 4) * 1.1
                print(f"{i} | {xp}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def heal(self, ctx):
        member = await db.get_member_class(self.client.pg_con, str(ctx.author.id))
        member.hp = member.max_hp
        await db.update_member_after_battle(self.client.pg_con, member)
        await ctx.send("You have been healed to full. (temp command)")


def setup(client):
    client.add_cog(Developer(client))
