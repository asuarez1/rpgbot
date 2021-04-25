class Buff:
    def __init__(self, member_id, value, turns, source, id=None):
        self.id = id
        self.member_id = member_id
        self.value = value
        self.turns = turns
        self.source = source


class FlatDmg(Buff):
    def get_flat_dmg_mod(self):
        return self.value


class PercentDmg(Buff):
    def get_percent_dmg_mod(self):
        self.turns -= 1
        return self.value


class CritChance(Buff):
    def get_crit_chance_mod(self):
        return self.value
