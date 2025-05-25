import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def fetch_concurrently():
    results = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    return results

# Example usage
if __name__ == "__main__":
    results = asyncio.run(fetch_concurrently())
    all_users, older_users = results
    print("All users:", all_users)
    print("Users older than 40:", older_users)