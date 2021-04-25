import discord
from discord.ext import commands
import db


class Battle(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['e', 'enc'])
    async def encounter(self, ctx):
        member_id = str(ctx.author.id)
        encounter = await db.get_encounter_class(self.client.pg_con, member_id, ctx)
        if encounter:
            if encounter.member.is_dead():
                await ctx.send("You are dead...")
            else:
                await encounter.send_embed()
        else:
            await self.generate_encounter(member_id)
            print(f"created a new encounter for {member_id}")
            encounter = await db.get_encounter_class(self.client.pg_con, member_id, ctx)
            await encounter.send_embed()

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def run(self, ctx):
        member_id = str(ctx.author.id)
        encounter = await db.get_encounter_class(self.client.pg_con, member_id, ctx)
        if encounter:
            await db.end_encounter(self.client.pg_con, encounter.id)
            await ctx.send("You got away safely.")
        else:
            await ctx.send("You do not have an active encounter.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['a', 'atk'])
    async def attack(self, ctx):
        member_id = str(ctx.author.id)
        encounter = await db.get_encounter_class(self.client.pg_con, member_id, ctx)
        if encounter:
            await encounter.attack()
        else:
            await ctx.send("You do not have an active encounter.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['s'])
    async def spell(self, ctx):
        member_id = str(ctx.author.id)
        encounter = await db.get_encounter_class(self.client.pg_con, member_id, ctx)
        if encounter:
            await encounter.buff()
        else:
            await ctx.send("You do not have an active encounter.")

    async def generate_encounter(self, member_id):
        await db.generate_encounter(self.client.pg_con, member_id)


def setup(client):
    client.add_cog(Battle(client))
