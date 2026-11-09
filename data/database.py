
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "environment.db"


def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                air_quality REAL
            )
        """)


def save_reading(reading):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            INSERT INTO sensor_readings
            (timestamp, temperature, humidity, air_quality)
            VALUES (?, ?, ?, ?)
        """, (
            reading["timestamp"],
            reading["temperature"],
            reading["humidity"],
            reading["air_quality"]
        ))


def get_readings():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute("""
            SELECT timestamp, temperature, humidity, air_quality
            FROM sensor_readings
            ORDER BY id ASC
        """)
        return cursor.fetchall()
