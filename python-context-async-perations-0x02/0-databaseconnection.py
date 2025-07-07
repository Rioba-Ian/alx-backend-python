"""
Create a class based context manager to handle
opening and closing database connections automatically
"""

import mysql.connector
import asyncio

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    async def __enter__(self):
        self.connection = await mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database=self.db_name
        )
        return self.connection

    async def __exit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    async def execute_query(self, query, params=None):
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()



db = DatabaseConnection("ALX.prodev")

async def main():
    async with db:
        await db.execute_query("SELECT * FROM users")

asyncio.run(main())
