import sqlite3

conn = sqlite3.connect('monitoring.db')
cursor = conn.cursor()

def display():
    cursor.execute('SELECT * FROM metrics')
    results = cursor.fetchall()
    for row in results:
        print(f"{row[0]} | CPU: {row[1]}% | RAM: {row[2]}% | Disque: {row[3]}%")

display()
