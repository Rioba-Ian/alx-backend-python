"""
create a reusable context manager that takes a query as input and executes it,
managing both connection and the query execution
"""


import mysql.connector
import asyncio


class ExecuteQuery:
  def __init__(self, query, params):
    self.query = query
    self.params = params


  async def __enter__(self):
    self.connection = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password",
      database="test"
    )
    self.cursor = self.connection.cursor()
    self.cursor.execute(self.query, self.params)
    return self.cursor


  async def __exit__(self, exc_type, exc_val, exc_tb):
    self.cursor.close()
    self.connection.close()



async def main():
  async with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as cursor:
    for row in cursor:
      print(row)

if __name__ == "__main__":
  asyncio.run(main())
