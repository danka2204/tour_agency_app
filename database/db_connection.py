import mysql.connector
from database.db_config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
