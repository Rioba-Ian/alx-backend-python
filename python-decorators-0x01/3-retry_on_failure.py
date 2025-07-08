"""
create a decorator that retries database operations if they fail due to transient errors
"""
import sqlite3
import functools
import os
import time

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
        conn = sqlite3.connect(DB_FILE)
        try:
            result = func(conn, *args, **kwargs)
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=1):

  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      for attempt in range(retries):
        try:
          return func(*args, **kwargs)
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
          if attempt < retries - 1:
            print(
              f"RETRY: Attempt {attempt + 1}/{retries} failed: {e}. Rertying in {delay} seconds..."
            )

          if 'database is locked' in str(e):
            time.sleep(delay)
          else:
            print(f"ERROR: Attempt {attempt + 1}/{retries} failed: {e}")
            raise
    return wrapper
  return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users")
  return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
