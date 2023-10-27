import os
import psycopg2
from dotenv import load_dotenv


class StorageManager:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def save_to_db(self, url, content):
        try:
            postgreSQL_insert_query = (
                """ INSERT INTO articles (url, content) VALUES (%s, %s)"""
            )
            self.cursor.execute(postgreSQL_insert_query, (url, content))
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting data", error)

    def fetch_articles(self):
        self.cursor.execute("SELECT id, url, content FROM articles")
        return self.cursor.fetchall()

    def update_article_summary(self, article_id, summary):
        self.cursor.execute(
            "UPDATE articles SET summary = %s WHERE id = %s", (summary, article_id)
        )
        self.connection.commit()


# # Usage
# if __name__ == "__main__":
#     storage_manager = StorageManager()
#     # storage_manager.save_to_db("url", "content")
#     articles = storage_manager.fetch_articles()
#     print(articles)
#     storage_manager.close()
