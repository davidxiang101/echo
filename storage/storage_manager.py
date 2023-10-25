import psycopg2


def save_to_db(url, content):
    try:
        connection = psycopg2.connect(
            user="username",
            password="password",
            host="127.0.0.1",
            port="5432",
            database="article_db",
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
