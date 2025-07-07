"""
Run multiple database queries concurrently using asyncio.gather
"""

import aiosqlite
import asyncio

async def async_fetch_users():
  async with aiosqlite.connect('users.db') as db:
    async with db.execute('SELECT * FROM users') as cursor:
      return await cursor.fetchall()

async def async_fetch_old_users():
  async with aiosqlite.connect('users.db') as db:
    async with db.execute('SELECT * FROM old_users WHERE age > 40') as cursor:
      return await cursor.fetchall()


results = asyncio.gather(async_fetch_users(), async_fetch_old_users())


async def fetch_concurrently():
  return await asyncio.gather(async_fetch_users(), async_fetch_old_users())

async def main():
  users, old_users = await fetch_concurrently()
  print(users)
  print(old_users)
