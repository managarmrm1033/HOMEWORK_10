import psycopg2
from pymongo import MongoClient

# Підключення до MongoDB
mongo_client = MongoClient('mongodb+srv://<username>:<password>@cluster0.vkganap.mongodb.net/')
mongo_db = mongo_client['test']  # Замінити на ім'я вашої БД
authors_collection = mongo_db['authors']  # Колекція авторів
quotes_collection = mongo_db['quotes']  # Колекція цитат

# Підключення до PostgreSQL
pg_conn = psycopg2.connect(
    dbname="postgres",  # Ім'я вашої бази в Postgres
    user="postgres",
    password="567234",
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Функція для міграції авторів
def migrate_authors():
    authors = authors_collection.find()  # Отримуємо авторів із MongoDB
    for author in authors:
        # Вставляємо авторів у PostgreSQL
        pg_cursor.execute(
            "INSERT INTO noteapp_author (name) VALUES (%s) RETURNING id",
            (author['name'],)
        )
        author_id = pg_cursor.fetchone()[0]  # Отримуємо новий ID автора

        # Міграція цитат для кожного автора
        migrate_quotes(author['_id'], author_id)

    pg_conn.commit()

# Функція для міграції цитат
def migrate_quotes(mongo_author_id, pg_author_id):
    quotes = quotes_collection.find({"author": mongo_author_id})
    for quote in quotes:
        pg_cursor.execute(
            "INSERT INTO noteapp_quote (text, author_id) VALUES (%s, %s)",
            (quote['text'], pg_author_id)
        )

# Виклик міграційних функцій
migrate_authors()

# Закриття з'єднань
pg_cursor.close()
pg_conn.close()
mongo_client.close()
