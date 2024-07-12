import psycopg2
from faker import Faker
try:
        db_postgres = psycopg2.connect(
            database = "db",
            user = "root",
            password = "root",
            host = "postgres",
            port = "5432"
        )
        print("POSTGRES BAGLANDI")
except psycopg2.Error as e:
        print(f"failed to connect to database: {e}")

table_queries = [
    '''CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        user_name TEXT NOT NULL,
        user_surname TEXT NOT NULL,
        user_address TEXT NOT NULL,
        user_nationality TEXT NOT NULL
    )''',

    '''CREATE TABLE IF NOT EXISTS orders(
        order_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        order_date DATE NOT NULL,
        order_amount DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''',

    '''CREATE TABLE IF NOT EXISTS user_profiles(
        profile_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        profile_picture TEXT,
        bio TEXT,
        date_of_birth DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )'''
]
# Table creation
for query in table_queries:
        with db_postgres.cursor() as cursor:
                cursor.execute(query)
                db_postgres.commit()

fake = Faker()
for _ in range(100):
        with db_postgres.cursor() as cursor:
            user_name = fake.first_name()
            user_surname = fake.last_name()
            user_address = fake.address()
            user_nationality = fake.country()
            cursor.execute(
                '''INSERT INTO users (user_name, user_surname, user_address, user_nationality) 
                VALUES (%s, %s, %s, %s) RETURNING user_id''', 
                (user_name, user_surname, user_address, user_nationality)
            )
            user_id = cursor.fetchone()[0]

            for _ in range (fake.random_int(min= 1, max=5)):
                    order_date = fake.date_this_year()
                    order_amount = fake.random_number(digits=2)
            cursor.execute(
                    '''INSERT INTO orders (user_id, order_date, order_amount) 
                    VALUES (%s, %s, %s)''', 
                    (user_id, order_date, order_amount)
                )
            profile_picture = fake.image_url()
            bio = fake.text(max_nb_chars=200)
            date_of_birth = fake.date_of_birth()
            cursor.execute(
                '''INSERT INTO user_profiles (user_id, profile_picture, bio, date_of_birth) 
                VALUES (%s, %s, %s, %s)''', 
                (user_id, profile_picture, bio, date_of_birth)
            )
            db_postgres.commit()
db_postgres.close()