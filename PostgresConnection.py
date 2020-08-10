import psycopg2
conn = psycopg2.connect(database="insert_database",
                        user="insert_user",
                        password="insert_password",
                        host="insert_host",
                        port="5432")
