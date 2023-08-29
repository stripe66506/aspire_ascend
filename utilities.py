import sqlite3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    conn = sqlite3.connect('database\central_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY,
        weekday TEXT NOT NULL,
        block TEXT NOT NULL,
        period TEXT NOT NULL,
        class_offered TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

setup_database()