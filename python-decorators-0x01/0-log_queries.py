"""
Decorator to log all SQL queries executed by a function.
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


#### decorator to lof SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query_arg = None

        if "query" in kwargs:
            query_arg = kwargs["query"]
        elif len(args) > 0:
            query_arg = args[0]

        if query_arg:
            print(f"Executing query: {query_arg}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
#
users = fetch_all_users(query="SELECT * FROM users")
print(users)

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
