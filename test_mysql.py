
import os
import mysql.connector
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

if connection.is_connected():
    print("MySQL Connected Successfully!")

connection.close()
