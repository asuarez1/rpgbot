import random


class Enemy:
    def __init__(self, enemy):
        self.id = enemy['enemy_id']
        self.name = enemy['enemy_desc']
        self.hp = enemy['hp']
        self.max_hp = enemy['max_hp']
        self.mp = enemy['mp']
        self.max_mp = enemy['max_mp']
        self.atk = enemy['attack']
        self.int = enemy['intelligence']
        self.atk_desc = ["bites", "scratches", "mauls", "tackles"]
        self.gold = enemy['gold']
        self.xp = enemy['xp']

    def battle_ai(self):
        pass

    def get_attack_desc(self):
        return random.choice(self.atk_desc)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0

    def is_dead(self):
        if self.hp == 0:
            return True
        else:
            return False


class Rat(Enemy):
    def battle_ai(self):
        pass
