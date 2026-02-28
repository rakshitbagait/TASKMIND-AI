import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="taskmind_ai",
    use_pure = True,
    port = 3306
)

cursor = conn.cursor()
print("Database connected successfully")

