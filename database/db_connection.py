import mysql.connector

def connect_db():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="waste2worth"
    )

    return conn