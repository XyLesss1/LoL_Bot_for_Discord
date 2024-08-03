import aiosqlite
import asyncio
name_bd = 'legendalitycs.db'
async def create_table_members(name_bd):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS members (user_id INTEGER PRIMARY KEY, global_name TEXT, "
                         "name TEXT, "
                             "tag TEXT, puuid TEXT)")
        await db.commit()
async def create_table_lol(name_bd_1):
    async with aiosqlite.connect(name_bd_1) as db:
        await db.execute(""" CREATE TABLE IF NOT EXISTS lol (
        puuid TEXT PRIMARY KEY,
        level INTEGER,
        rank TEXT,
        top_champs TEXT,
        FOREIGN KEY (puuid) REFERENCES members (puuid))
        """)
async def create_line (user_id, global_name, name, tag, puuid):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute("INSERT INTO members (user_id, global_name, name, tag, puuid) VALUES (?, ?, ?, ?, "
                             "?)", (user_id, global_name, name, tag, puuid))
        await db.commit()

async def create_line_lol(puuid, level, rank, champs):
    async with aiosqlite.connect(name_bd) as db:
        await db.execute("""INSERT INTO lol (
        puuid,
        level,
        rank,
        top_champs)
        VALUES (?, ?, ?, ?)
        """, (puuid, level, rank, champs))
        await db.commit()

async def get_stats_lol(user_id):
    async with aiosqlite.connect('legendalitycs.db') as db:
        async with db.execute(f'SELECT * FROM members WHERE user_id = {user_id}') as cursor:
            rows = await cursor.fetchone()
            puuid = rows[-1]
            async with db.execute(f"SELECT * from lol WHERE puuid = '{puuid}'") as crsr:
                row = await crsr.fetchone()
                return row
