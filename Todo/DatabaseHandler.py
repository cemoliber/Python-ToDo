import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db="todo.db"):
        # Database Connection
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create table if needed
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                openDate TEXT NOT NULL,
                daysOpen INTEGER NOT NULL,
                content TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def delete_data(self, item_id):
        # Veritabanından satırı silme
        self.cursor.execute("DELETE FROM todo WHERE id = ?", (item_id,))
        self.conn.commit()

    def add_data(self, title, status, open_date, days_open, content):
        query = '''INSERT INTO todo (title, status, openDate, daysOpen, content)
                   VALUES (?, ?, ?, ?, ?)'''
        print(title, status, open_date, days_open, content)
        self.cursor.execute(query, (title, status, open_date, days_open, content))
        self.conn.commit()

    def update_data(self, record_id, title, status, open_date, days_open, content):
        # SQL UPDATE komutuyla veritabanını güncelle
        query = """
        UPDATE todo 
        SET title = ?, status = ?, openDate = ?, daysOpen = ?, content = ? 
        WHERE id = ?
        """

        if(status == 'Done'):
            self.cursor.execute(query, (title, status, open_date, days_open, content, record_id))
            self.conn.commit()
        else:
            self.cursor.execute(query, (title, status, open_date, -1, content, record_id))
            self.conn.commit()
        
        
    def date_control(self, record_id, days_open):
        query = """
        UPDATE your_table_name
        SET b_column = ?
        WHERE id = ?
        """
        self.cursor.execute(query, (days_open, record_id))

    def filter_datas(self, status):
        self.cursor.execute("SELECT * FROM todo WHERE status = ?", (status,))
        return self.cursor.fetchall()

    def fetch_all_data(self):
        # Fetch all datas
        self.cursor.execute("SELECT * FROM todo")
        return self.cursor.fetchall()

    def close(self):
        # Close the connection
        self.conn.close()
