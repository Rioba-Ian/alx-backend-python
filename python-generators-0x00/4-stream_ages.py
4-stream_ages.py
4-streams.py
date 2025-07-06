"""
Memory-efficient average age calculator using Python generators.
"""

import mysql.connector

def stream_user_ages():
  connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="mydatabase"
  )
  cursor = connection.cursor()
  cursor.execute("SELECT age FROM users")
  for row in cursor:
    yield row[0]
  cursor.close()
  connection.close()


def compute_average_age():
  total_age = 0
  count = 0
  for age in stream_user_ages():
    total_age += age
    count += 1
  return total_age / count if count > 0 else 0
