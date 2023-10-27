import os
import psycopg2
from dotenv import load_dotenv


def save_to_db(url, content):
    load_dotenv()
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()
        postgreSQL_insert_query = (
            """ INSERT INTO articles (url, content) VALUES (%s, %s)"""
        )
        cursor.execute(postgreSQL_insert_query, (url, content))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
