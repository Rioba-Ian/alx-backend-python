"""
create a decorator that manages database transactions by automatically committing or rolling back changes
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
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            print("INFO: DB Connection established")
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
          if conn:
            conn.rollback()
            raise e
        finally:
          if conn:
            conn.close()
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
        except Exception as e:
            print(f"TRANSACTION FAILED: An error occurred, rolling back. {e}")
            conn.rollback()
            raise e
        else:
            print("TRANSACTION SUCCESSFUL")
        return result
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
  cursor = conn.cursor()
  cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
#### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
