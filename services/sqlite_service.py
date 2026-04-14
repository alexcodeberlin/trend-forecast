import sqlite3

DB = "data.db"

class SQLiteService:

    def save(self, x, y):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data (x TEXT, y REAL)")
        for i, j in zip(x, y):
            c.execute("INSERT INTO data VALUES (?,?)", (i, j))
        conn.commit()
        conn.close()

    def get_all(self):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM data")
        rows = c.fetchall()
        conn.close()
        return rows