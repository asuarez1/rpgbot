import math
from random import randint

import combat.buffs


class Member:
    def __init__(self, member, weapon, buffs):
        self.id = member['member_id']
        self.lvl = member['lvl']
        self.xp = member['xp']
        self.gold = member['gold']
        self.skill_points = member['skill_points']
        self.hp = member['hp']
        self.max_hp = member['vigor'] * 5
        self.mp = member['mp']
        self.max_mp = member['spirit'] * 5
        self.str = member['strength']
        self.dex = member['dexterity']
        self.int = member['intelligence']
        self.luck = member['luck']
        self.vig = member['vigor']
        self.spt = member['spirit']
        self.weapon = weapon
        self.buffs = buffs
        self.crit = False

    def get_xp_needed(self):
        xp = 0
        for i in range(0, self.lvl):
            if i == 0:
                xp = 100
            else:
                xp += (xp / 4) * 1.1
        return math.floor(xp)

    def check_lvl_up(self):
        xp_needed = self.get_xp_needed()
        lvls_gained = 0
        while self.xp >= xp_needed:
            self.lvl += 1
            self.xp -= xp_needed
            self.skill_points += 2
            xp_needed = self.get_xp_needed()
            lvls_gained += 1
        return lvls_gained

    def get_dmg(self):
        base_dmg = self.weapon.base_damage
        return math.floor((base_dmg + self.get_fmod()) * self.get_pmod() * self.is_crit())

    def get_pmod(self):
        mod = 0
        if self.weapon.style == "MELEE":
            mod += self.str * 5 / 100
        elif self.weapon.style == "RANGED":
            mod += self.dex * 5 / 100

        for b in self.buffs:
            if isinstance(b, combat.buffs.PercentDmg):
                mod += int(b.get_percent_dmg_mod())

        return 1 + mod

    def get_fmod(self):
        return 0

    def get_crit_chance(self):
        return 0 + self.luck

    def is_crit(self):
        if self.get_crit_chance() >= randint(1, 100):
            self.crit = True
            return 2
        else:
            return 1

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0

    def is_dead(self):
        if self.hp == 0:
            return True
        else:
            return False
