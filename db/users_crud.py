import aiosqlite
import asyncio
async def create_user(id_tg: int):
    async with aiosqlite.connect('lead.db') as conn:
        await conn.execute('INSERT INTO users (id_tg) VALUES (?)', (id_tg,))
        await conn.commit()
    return True

async def get_user(id_tg: int):
    async with aiosqlite.connect('lead.db') as conn:
        cursor = await conn.execute('SELECT * FROM users WHERE id_tg = ?', (id_tg,))
        return await cursor.fetchone()
    
async def update_user(id_tg: int, **kwargs):
    async with aiosqlite.connect('lead.db') as conn:
        for parameter, value in kwargs.items():
            await conn.execute(f'UPDATE users SET {parameter} = ? WHERE id_tg = ?', (value, id_tg))
        await conn.commit()
    return True

async def delete_user(id_tg: int):
    async with aiosqlite.connect('lead.db') as conn:
        await conn.execute('DELETE FROM users WHERE id_tg = ?', (id_tg,))
        await conn.commit()
    return True

if __name__ == "__main__":
    asyncio.run(update_user(431425615, name="test1", phone="test2"))