import sqlite3

conn = sqlite3.connect('monitoring.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS metrics (timestamp TEXT cpu INTEGER, ram INTEGER, disk INTEGER);')
cursor.clean()
conn.commit()

def clean():
    limite = datetime.datetime.now() - datetime.timedelta(hours=24)
    cursor.execute('DELETE FROM metrics WHERE timestamp < ?', (limite.isoformat(),))
    conn.commit()

cursor.execute('SELECT * FROM metrics')
result = cursor.fetchall()
if result{
  print(f'Date et heure: {result[0]}, CPU: {result[1]} %, RAM: {result[2]} %, DISK: {result[3]} %')
} else {
  print("Aucune donnée.")
}
