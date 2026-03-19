import sqlite3

conn = sqlite3.connect('monitoring.db')
cursor = conn.cursor()

def display():
    cursor.execute('SELECT * FROM metrics')
    results = cursor.fetchall()
    for row in results:
        print(f"MACHINE: {row[4]} | {row[0]} | CPU: {row[1]}% | RAM: {row[2]}% | Disque: {row[3]}%")
    cursor.execute('SELECT * FROM alertes ORDER BY rowid DESC LIMIT 1')
    result = cursor.fetchone()
    print(f"Dernière alerte : {result[0]} | Lien : {result[1]}")

display()
