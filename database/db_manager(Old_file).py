import mysql.connector
from mysql.connector import Error
from . import db_config


class DBManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=db_config.host,
                user=db_config.user,
                password=db_config.password,
                database=db_config.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print("Помилка підключення до БД:", e)

    # Отримати всіх клієнтів
    def get_clients(self):
        self.cursor.execute("SELECT * FROM Client")
        return self.cursor.fetchall()

    # Додати клієнта
    def add_client(self, name, phone):
        sql = "INSERT INTO Client (clientName, clientPhone) VALUES (%s, %s)"
        self.cursor.execute(sql, (name, phone))
        self.connection.commit()

    # Оновити клієнта
    def update_client(self, client_id, name, phone):
        sql = "UPDATE Client SET clientName=%s, clientPhone=%s WHERE clientId=%s"
        self.cursor.execute(sql, (name, phone, client_id))
        self.connection.commit()

    # Видалити клієнта
    def delete_client(self, client_id):
        sql = "DELETE FROM Client WHERE clientId=%s"
        self.cursor.execute(sql, (client_id,))
        self.connection.commit()

    def __del__(self):
        if hasattr(self, "connection"):
            self.cursor.close()
            self.connection.close()
