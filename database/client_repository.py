from database.db_connection import get_connection

class ClientRepository:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def create_client(self, name, phone):
        sql = "INSERT INTO Client (clientName, clientPhone) VALUES (%s, %s)"
        self.cursor.execute(sql, (name, phone))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM Client")
        return self.cursor.fetchall()

    def update_client(self, client_id, name, phone):
        sql = """
            UPDATE Client
            SET clientName=%s, clientPhone=%s
            WHERE clientId=%s
        """
        self.cursor.execute(sql, (name, phone, client_id))
        self.conn.commit()

    def delete_client(self, client_id):
        sql = "DELETE FROM Client WHERE clientId=%s"
        self.cursor.execute(sql, (client_id,))
        self.conn.commit()

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass
