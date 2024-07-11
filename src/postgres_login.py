import psycopg2
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

        