import aiosqlite

async def create_user(id_tg: int):
    async with aiosqlite.connect('lead.db') as conn:
        await conn.execute('INSERT INTO users (id_tg) VALUES (?)', (id_tg,))
        await conn.commit()
    return True

async def get_user(id_tg: int):
    async with aiosqlite.connect('lead.db') as conn:
        cursor = await conn.execute('SELECT * FROM users WHERE id_tg = ?', (id_tg,))
        return await cursor.fetchone()
    
async def update_user(id_tg: int, name: str):
    async with aiosqlite.connect('lead.db') as conn:
        await conn.execute('UPDATE users SET name = ? WHERE id_tg = ?', (name, id_tg))
        await conn.commit()
    return True