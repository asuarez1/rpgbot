import inspect

import combat.encounters
import combat.weapons as wpn
import combat.enemies as enm
import combat.member as mem
import combat.buffs as bf


def create_dict(module, klass):
    d = {}
    for name, cls in inspect.getmembers(module):
        if inspect.isclass(cls) and issubclass(cls, klass):
            if cls != klass:
                d[cls.__name__] = cls
    return d


async def get_member(pg_con, member_id):
    member = await pg_con.fetchrow("SELECT * FROM member_view WHERE member_id = $1", member_id)
    return member


async def get_member_class(pg_con, member_id):
    member = await pg_con.fetchrow("SELECT * FROM member_view WHERE member_id = $1", member_id)
    weapon = await get_member_weapon(pg_con, member_id)
    buffs = await get_buffs(pg_con, member_id)
    return mem.Member(member, weapon, buffs)


async def get_members(pg_con, member_id):
    member = await pg_con.fetch("SELECT * FROM member_view WHERE member_id = $1", member_id)
    return member


async def add_member(pg_con, member_id):
    sql = f"INSERT INTO members (member_id) VALUES (\'{member_id}\')"
    await pg_con.execute(sql)


async def update_member_after_battle(pg_con, member):
    sql = """
            UPDATE 	member_stats 
            SET 	hp = $1,
                    mp = $2,
                    skill_points = $3
            WHERE member_id = $4
            """
    await pg_con.execute(sql, member.hp, member.mp, member.skill_points, member.id)

    sql = """
            UPDATE 	members 
            SET 	lvl = $1,
                    xp = $2,
                    gold = $3
            WHERE member_id = $4
            """

    await pg_con.execute(sql, member.lvl, member.xp, member.gold, member.id)


async def update_enemy_after_battle(pg_con, enemy):
    sql = f"UPDATE enemies SET hp = {enemy.hp}, mp = {enemy.mp}" \
          f"WHERE enemy_id = \'{enemy.id}\'"
    await pg_con.execute(sql)


async def update_skill(pg_con, member_id, skill, skill_value, sp_value):
    sql = f"UPDATE member_stats SET {skill} = {skill_value}, skill_points = {sp_value}" \
          f"WHERE member_id = \'{member_id}\'"
    await pg_con.execute(sql)


async def get_rand_enemy(pg_con):
    sql = "SELECT * FROM enemy_types ORDER BY RANDOM() LIMIT 1"
    return await pg_con.fetchrow(sql)


async def get_enemy(pg_con, enemy_id):
    sql = f"SELECT * FROM enemies WHERE enemy_id = {enemy_id}"
    return await pg_con.fetchrow(sql)


async def get_enemy_class(pg_con, encounter_id):
    sql = f"SELECT * FROM enemy_view WHERE encounter_id = {encounter_id}"
    enemy = await pg_con.fetchrow(sql)
    d = create_dict(enm, enm.Enemy)
    return d[enemy['ai']](enemy)


async def add_enemy(pg_con, encounter_id, enemy_type):
    sql = f"INSERT INTO enemies (enemy_type_id, encounter_id, hp, mp)" \
          f"VALUES ({enemy_type['enemy_type_id']}, {encounter_id}, {enemy_type['max_hp']}, {enemy_type['max_mp']})"
    await pg_con.execute(sql)


async def get_active_encounter(pg_con, member_id):
    sql = f"SELECT * FROM encounters WHERE member_id = \'{member_id}\' AND is_active = true"
    return await pg_con.fetchrow(sql)


async def add_encounter(pg_con, member_id):
    # print(enemy)
    sql = f"INSERT INTO encounters (member_id)" \
          f"VALUES (\'{member_id}\')"
    await pg_con.execute(sql)


async def end_encounter(pg_con, encounter_id):
    sql = f"UPDATE encounters SET is_active = false WHERE encounter_id = {encounter_id}"
    await pg_con.execute(sql)


async def get_member_weapon(pg_con, member_id):
    sql = f"SELECT 		w.* FROM		    members as m LEFT JOIN	    weapons as w    ON w.weapon_id = m.weapon_id " \
          f"WHERE 		    m.member_id = '{member_id}' "

    weapon = await pg_con.fetchrow(sql)
    return wpn.Weapon(weapon)


async def generate_encounter(pg_con, member_id):
    # create encounter
    await add_encounter(pg_con, member_id)
    encounter = await get_active_encounter(pg_con, member_id)
    # get enemy type
    enemy_type = await get_rand_enemy(pg_con)
    # add enemy
    await add_enemy(pg_con, encounter['encounter_id'], enemy_type)


async def get_encounter_class(pg_con, member_id, ctx):
    active_encounter = await get_active_encounter(pg_con, member_id)
    if active_encounter:
        enemy = await get_enemy_class(pg_con, active_encounter['encounter_id'])
        member = await get_member_class(pg_con, member_id)
        encounter = combat.encounters.Encounter(active_encounter['encounter_id'], member, enemy, pg_con, ctx)
        return encounter
    else:
        return False


async def get_kill_stats(pg_con, member_id):
    sql = """   SELECT 		ev.enemy_desc,
                            COUNT(ev.enemy_id) AS kills
                FROM 		enemy_view ev
                LEFT JOIN 	encounters e 		ON e.encounter_id = ev.encounter_id
                WHERE 		ev.hp = 0
                AND 		e.member_id = $1
                GROUP BY	ev.enemy_desc;   """
    return await pg_con.fetch(sql, member_id)


async def get_buffs(pg_con, member_id):
    sql = """   SELECT 		*
                FROM 		buffs 
                WHERE 		turns > 0
                AND         member_id = $1
                """
    records = await pg_con.fetch(sql, member_id)
    d = create_dict(bf, bf.Buff)
    buffs = []

    for r in records:
        buffs.append(d[r['method']](r['member_id'], r['value'], r['turns'], r['source'], r['buff_id']))

    return buffs


async def update_buffs(pg_con, buff):
    if buff.id:
        sql = """
                UPDATE  buffs
                SET     turns = $1
                WHERE   buff_id = $2
                """
        await pg_con.execute(sql, buff.turns, buff.id)
    else:
        sql = """
                INSERT INTO buffs 	(member_id, value, turns, source, method)
                VALUES 				($1, $2, $3, $4, $5)

                """
        await pg_con.execute(sql, buff.member_id, buff.value, buff.turns, buff.source, type(buff).__name__)
