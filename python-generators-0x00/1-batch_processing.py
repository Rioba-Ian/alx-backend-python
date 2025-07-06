"""
Write a function stream_users_in_batches(batch_size) that fetches rows in batches

Write a function batch_processing() that processes each batch to filter users over the age of25`
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password",
      database="mydatabase"
    )
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM users")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def batch_processing():
    for batch in stream_users_in_batches(100):
        filtered_batch = [user for user in batch if user[2] > 25]
        print(f"Processed batch: {filtered_batch}")
