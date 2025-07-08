"""
create a decorator that caches the results of a database queries inorder to avoid redundant calls
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


query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE)
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper



def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print(f"Query '{query}' is cached")
            return query_cache[query]
        result = func(conn, query)
        print(f"Query '{query}' is executed and being cached...")
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
