import aiosqlite
from config.config import TAGS
async def create_user_tag(user_id: int, tag_name: str):
    if tag_name in TAGS:
        async with aiosqlite.connect('lead.db') as conn:
            cur = await conn.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
            tag_id = await cur.fetchone()
            await conn.execute('INSERT INTO users_tags (user_id, tag_id) VALUES (?, ?)', (user_id, tag_id[0]))
            await conn.commit()
            return True
    return False
