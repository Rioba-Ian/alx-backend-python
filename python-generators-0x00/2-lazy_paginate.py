"""
Implement a generator function lazypaginate(pagesize) that implements the paginate_users(page_size, offset) that will only fetch the next page when needed at an offset of 0.
"""

import mysql.connector

def paginate_users(pagesize, offset=0):
  connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="users"
  )
  cursor = connection.cursor()

  try:
    cursor.execute("SELECT * FROM users LIMIT %s OFFSET %s", (pagesize, offset))
    users = cursor.fetchall()
    yield users
  except mysql.connector.Error as err:
    print(f"Error: {err}")
  finally:
    cursor.close()
    connection.close()


def lazy_pagination(pagesize):
  offset = 0
  while True:
    users = next(paginate_users(pagesize, offset), None)
    if users is None:
      break
    yield users
    offset += pagesize
