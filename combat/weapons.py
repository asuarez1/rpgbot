import random


class Weapon:
    def __init__(self, weapon):
        self.id = weapon['weapon_id']
        self.desc = weapon['weapon_desc']
        self.base_damage = weapon['base_damage']
        self.damage_type = weapon['damage_type_id']
        self.style = weapon['weapon_style']
        self.atk_desc = ["punches", "clobbers", "swings at", "wallops"]

    def get_attack_desc(self):
        return random.choice(self.atk_desc)


# Default Weapon

class Fists(Weapon):
    pass


# Rookie Weapons

class RookieSword(Weapon):
    pass


class RookieMace(Weapon):
    pass


class RookieLance(Weapon):
    pass


class RookieBow(Weapon):
    pass
