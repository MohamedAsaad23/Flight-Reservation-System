import sqlite3

class Database:
    def __init__(self, db_name="DATABASE.db"):

        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # ---- Airports ----
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS airports (
                name TEXT PRIMARY KEY
            )
        """)
        # ---- Flights ----
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                src TEXT,
                dest TEXT,
                cost REAL,
                PRIMARY KEY (src, dest),
                FOREIGN KEY(src) REFERENCES airports(name) ON DELETE CASCADE,
                FOREIGN KEY(dest) REFERENCES airports(name) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    # ---- Check if airport exists ----
    def airport_exists(self, name):
        self.c.execute("SELECT 1 FROM airports WHERE name=?", (name,))
        return self.c.fetchone() is not None

    # ---- Airports ----
    def add_airport(self, name):
        if self.airport_exists(name):
            return "exists"
        try:
            self.c.execute("INSERT INTO airports (name) VALUES (?)", (name,))
            self.conn.commit()
            return "success"
        except sqlite3.Error:
            return "error"

    def delete_airport(self, name):
        if not self.airport_exists(name):
            return "not_found"
        try:
            self.c.execute("DELETE FROM airports WHERE name=?", (name,))
            self.conn.commit()
            return "success"
        except sqlite3.Error:
            return "error"

    def get_airports(self):
        self.c.execute("SELECT name FROM airports ORDER BY name")
        return [row[0] for row in self.c.fetchall()]


    # ---- Flights ----
    def flight_exists(self, src, dest):
        self.c.execute("SELECT 1 FROM flights WHERE src=? AND dest=?", (src, dest))
        return self.c.fetchone() is not None

    def add_flight(self, src, dest, cost):
        if not self.airport_exists(src) or not self.airport_exists(dest):
            return "no_airport"
        if self.flight_exists(src, dest):
            return "exists"
        try:
            self.c.execute("INSERT INTO flights (src, dest, cost) VALUES (?, ?, ?)", (src, dest, cost))
            self.conn.commit()
            return "success"
        except sqlite3.Error:
            return "error"

    def delete_flight(self, src, dest):
        if not self.flight_exists(src, dest):
            return "not_found"
        try:
            self.c.execute("DELETE FROM flights WHERE src=? AND dest=?", (src, dest))
            self.conn.commit()
            return "success"
        except sqlite3.Error:
            return "error"

    def get_flights(self):
        self.c.execute("SELECT src, dest, cost FROM flights ORDER BY src, dest")
        return self.c.fetchall()

    def close(self):
        self.conn.close()
