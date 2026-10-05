import os
import mysql.connector


def db():
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST", "mariadb"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "travel_destinations")
        )

        cursor = db.cursor(dictionary=True)
        return db, cursor

    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)