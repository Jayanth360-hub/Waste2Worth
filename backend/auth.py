from database.db_connection import connect_db

def signup(username,email,password):

    conn = connect_db()
    cursor = conn.cursor()

    query = "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)"
    cursor.execute(query,(username,email,password))
    

    conn.commit()
    conn.close()


def login(email,password):

    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query,(email,password))

    user = cursor.fetchone()

    conn.close()

    return user