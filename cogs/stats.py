import discord
import db
import cv
from discord.ext import commands
from prettytable import prettytable


class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx):
        member_id = str(ctx.author.id)
        member = await db.get_member(self.client.pg_con, member_id)
        xp = await db.get_member_class(self.client.pg_con, member_id)
        t = prettytable.PrettyTable()
        t.field_names = ["Skill Points:", f"{member['skill_points']}"]
        t.add_rows(
            [["HP", f"{member['hp']}/{member['vigor'] * 5}"],
             ["MP", f"{member['mp']}/{member['spirit'] * 5}"],
             ["Level", member['lvl']],
             ["Experience", f"{member['xp']}/{xp.get_xp_needed()}"],
             ["Strength", member['strength']],
             ["Dexterity", member['dexterity']],
             ["Intelligence", member['intelligence']],
             ["Luck", member['luck']],
             ["Vigor", member['vigor']],
             ["Spirit", member['spirit']]])
        t.align = "l"
        # await ctx.send(f"{ctx.author.mention}**\'s Stats**\n`{t}`")

        embed = discord.Embed(description=f"`{t}`", color=0xc33232)
        embed.set_author(name=f"{ctx.author.name}\'s Stats", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sp'])
    async def skillpoint(self, ctx, skill: cv.IsSkillConverter, points: cv.PosIntConverter):
        member_id = str(ctx.author.id)
        member = await db.get_member(self.client.pg_con, member_id)
        if points <= member['skill_points']:
            skill_value = member[skill] + points
            sp_value = member['skill_points'] - points
            await db.update_skill(self.client.pg_con, member_id, skill, skill_value, sp_value)
            await ctx.send("Skill points allocated.")
        else:
            await ctx.send("You do not have enough skill points.")

    @commands.command()
    async def kills(self, ctx):
        records = await db.get_kill_stats(self.client.pg_con, str(ctx.author.id))
        t = prettytable.PrettyTable()
        t.field_names = ["Enemy", "Times Killed"]
        for r in records:
            t.add_row([r['enemy_desc'], r['kills']])
        t.align = "l"
        embed = discord.Embed(description=f"`{t}`", color=0xc33232)
        embed.set_author(name=f"{ctx.author.name}\'s Kill Stats", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Stats(client))
