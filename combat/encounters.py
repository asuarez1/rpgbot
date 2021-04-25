import discord

import db
from combat import buffs


class Encounter:
    def __init__(self, encounter_id, member, enemy, pg_con, ctx):
        self.id = encounter_id
        self.member = member
        self.enemy = enemy
        self.embed_desc = ""
        self.embed_footer = f"A {self.enemy.name} stands before you. What will you do?"
        self.pg_con = pg_con
        self.ctx = ctx

    async def send_embed(self):
        embed = discord.Embed(description=self.embed_desc)
        embed.set_author(name=f"{self.ctx.author.name}\'s Encounter", icon_url=self.ctx.author.avatar_url)
        embed.add_field(name=f"{self.enemy.name}", value=f"HP: {self.enemy.hp}/{self.enemy.max_hp}", inline=True)
        embed.add_field(name=f"{self.ctx.author.name}", value=f"HP: {self.member.hp}/{self.member.max_hp}\n"
                                                              f"MP: {self.member.mp}/{self.member.max_mp}",
                        inline=False)
        embed.set_footer(text=self.embed_footer)
        await self.ctx.send(embed=embed)

    async def attack(self):
        member_dmg = self.member.get_dmg()
        self.enemy.take_damage(member_dmg)
        self.embed_desc = f"{self.ctx.author.name} {self.member.weapon.get_attack_desc()} {self.enemy.name} " \
                          f"with their {self.member.weapon.desc} "
        if self.member.crit:
            self.embed_desc += f"and deals a **critical** for **{member_dmg}** damage!\n "
        else:
            self.embed_desc += f"and deals {member_dmg} damage!\n "

        if self.enemy.is_dead():
            await self.on_enemy_dead()
            return

        await self.enemy_turn()

        if self.member.is_dead():
            self.embed_footer = "You have been slain. Hopefully i\'ll implement resurrection soon."
            await db.end_encounter(self.pg_con, self.id)
            await self.update_db()
            await self.send_embed()
            return

        await self.update_db()
        await self.send_embed()

    async def buff(self):
        self.embed_desc = f"{self.ctx.author.name} casts Soul Strike, increasing their damage for their next attack.\n"
        buff = buffs.PercentDmg(self.member.id, 10, 1, "Soul Strike")
        self.member.buffs.append(buff)
        await self.enemy_turn()

        if self.member.is_dead():
            self.embed_footer = "You have been slain. Hopefully i\'ll implement resurrection soon."
            await self.end_encounter()
            await self.update_db()
            await self.send_embed()
            return

        await self.update_db()
        await self.send_embed()

    async def update_db(self):
        await db.update_member_after_battle(self.pg_con, self.member)
        await db.update_enemy_after_battle(self.pg_con, self.enemy)
        for b in self.member.buffs:
            await db.update_buffs(self.pg_con, b)

    async def on_enemy_dead(self):
        self.embed_desc += f"{self.enemy.name} was slain!"
        self.embed_footer = f"You gained {self.enemy.gold} gold.\n" \
                            f"You gained {self.enemy.xp} xp."
        self.member.gold += self.enemy.gold
        self.member.xp += self.enemy.xp
        lvls_gained = self.member.check_lvl_up()
        await self.end_encounter()
        if lvls_gained > 0:
            await self.ctx.send(f"You went up {lvls_gained} level(s) from this battle!\n"
                                f"You have {self.member.skill_points} skill points available to spend.")

    async def enemy_turn(self):
        enemy_dmg = self.enemy.atk
        self.member.take_damage(enemy_dmg)
        self.embed_desc += f"{self.enemy.name} {self.enemy.get_attack_desc()} {self.ctx.author.name} " \
                           f"and deals {enemy_dmg} damage!\n"

    async def end_encounter(self):
        for b in self.member.buffs:
            b.turns = 0

        await db.end_encounter(self.pg_con, self.id)
        await self.update_db()
        await self.send_embed()


