from database.db_connection import get_connection

class TourRepository:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def create_tour(self, name, route, start_date, duration, price):
        sql = """
            INSERT INTO Tour (tourName, route, startDate, duration, price)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (name, route, start_date, duration, price))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_tours(self):
        self.cursor.execute("SELECT * FROM Tour")
        return self.cursor.fetchall()

    def update_tour(self, tour_id, name, route, start_date, duration, price):
        sql = """
            UPDATE Tour
            SET tourName=%s, route=%s, startDate=%s, duration=%s, price=%s
            WHERE tourId=%s
        """
        self.cursor.execute(sql, (name, route, start_date, duration, price, tour_id))
        self.conn.commit()

    def delete_tour(self, tour_id):
        sql = "DELETE FROM Tour WHERE tourId=%s"
        self.cursor.execute(sql, (tour_id,))
        self.conn.commit()

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass
