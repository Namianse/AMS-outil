import sqlite3
import datetime
import json

conn = sqlite3.connect('monitoring.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS metrics 
              (timestamp TEXT, cpu REAL, ram REAL, disque_pct REAL)''')
conn.commit()

with open('cpu_ram.json', 'r') as f:
    cpu_ram = json.load(f)

with open('disque.json', 'r') as f:
    disque = json.load(f)

def clean():
    limite = datetime.datetime.now() - datetime.timedelta(hours=24)
    cursor.execute('DELETE FROM metrics WHERE timestamp < ?', (limite.isoformat(),))
    conn.commit()

def insert():
    cursor.execute('INSERT INTO metrics VALUES (?, ?, ?, ?)', (
        cpu_ram['timestamp'],
        cpu_ram['cpu'],
        cpu_ram['ram'],
        disque['disque_pct']
    ))
    conn.commit()

clean()
insert()
