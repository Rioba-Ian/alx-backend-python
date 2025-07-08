"""
create a decorator that automatically handles opening and closing database connections
"""
import sqlite3
import functools
import os

# -- create dummy database for the example
DB_FILE = 'users.db'
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
cursor.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Jane Doe', 'jane@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Bob Smith', 'bob@example.com')")
conn.commit()
conn.close()

def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      conn = None
      try:
        conn = sqlite3.connect(DB_FILE)
        print("INFO: Opening database connection")
        return func(conn, *args, **kwargs)
      finally:
        if conn:
          conn.close()

    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
  return cursor.fetchone()
#### Fetch user by ID with automatic connection handling

user = get_user_by_id(user_id=1)
print(user)
