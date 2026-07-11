from database.db_connection import connect_db

def save_prediction(email, moisture, fiber, impurity, color, odor, storage, result):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions 
        (email, moisture, fiber, impurity, color, odor, storage, result)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (email, moisture, fiber, impurity, color, odor, storage, result))

    conn.commit()
    conn.close()