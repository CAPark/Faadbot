#test code provided by pynative.com guide on mysql connections in python
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host = 'localhost',
                                        database = 'testDB',
                                        user = 'root',
                                        password = '')#enter your password here
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MYSQL Server Version ", db_Info)
        cursor = connection.cursor()

        cursor.execute("Select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")