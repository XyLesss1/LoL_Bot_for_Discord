import aiosqlite
import asyncio

name_bd = 'legendalitycs.db'


async def create_table_members(name_bd):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS members (user_id INTEGER PRIMARY KEY, global_name TEXT, "
                         "name TEXT,"
                         "tag TEXT, puuid TEXT, region TEXT)")
        await db.commit()


async def create_line(user_id, global_name, name, tag, puuid, region):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute("INSERT INTO members (user_id, global_name, name, tag, puuid, region) VALUES (?, ?, ?, ?, "
                         "?, ?)", (user_id, global_name, name, tag, puuid, region))
        await db.commit()


async def get_puuid(user_id):
    async with aiosqlite.connect('legendalitycs.db') as db:
        async with db.execute(f'SELECT * FROM members WHERE user_id = {user_id}') as cursor:
            rows = await cursor.fetchone()
            puuid = rows[-2]
            return puuid


async def get_region(user_id):
    async with aiosqlite.connect('legendalitycs.db') as db:
        async with db.execute(f'SELECT * FROM members WHERE user_id = {user_id}') as cursor:
            rows = await cursor.fetchone()
            region = rows[-1]
            return region


async def update():
    async with aiosqlite.connect('legendalitycs.db') as db:
        await db.execute(""" UPDATE members
        SET region = 'EUW1'
        WHERE region = 'EUW'
        """)
        await db.commit()


async def create_table(name_bd):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
         user_id,
         warns INTEGER)""")


async def add_warn(user_id):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute(f"""UPDATE users
        SET warns = warns + 1
        WHERE user_id = {user_id}""")
        await db.commit()


async def get_warns(user_id):
    async with aiosqlite.connect(name_bd) as db:
        async with db.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""") as cursor:
            row = await cursor.fetchall()
            return row[0][1]


async def create_line_users(user_id):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute(f"""INSERT INTO users (user_id, warns) VALUES (?,?)""", (user_id, 0))
        await db.commit()

