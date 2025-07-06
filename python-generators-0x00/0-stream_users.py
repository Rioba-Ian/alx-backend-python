
import mysql.connector


try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mydatabase"
    )
    cursor = connection.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

def stream_users():
  try :
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        yield row
  except mysql.connector.Error as err:
      print(f"Error: {err}")
  finally:
    cursor.close()
    connection.close()
