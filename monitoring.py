import urllib.request
import xml.etree.ElementTree as ET
import sqlite3
import datetime
import json

conn = sqlite3.connect('/home/dieu/AMS-outil/monitoring.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS metrics 
              (timestamp TEXT, cpu REAL, ram REAL, disque_pct REAL)''')
conn.commit()

response = urllib.request.urlopen('https://www.cert.ssi.gouv.fr/feed/')
root = ET.parse(response).getroot()

items = root.findall('.//item')
item  = items[-1]
titre = item.find('title').text.strip()
lien  = item.find('link').text.strip()

cursor.execute('SELECT 1 FROM alertes WHERE lien = ?', (lien,))
if cursor.fetchone() is None:
    cursor.execute('INSERT INTO alertes VALUES (?, ?)', (titre, lien))
    conn.commit()
    print(f"Nouvelle alerte : {titre}")

cursor.execute('''CREATE TABLE IF NOT EXISTS alertes
              (titre TEXT, lien TEXT)''')
conn.commit()

with open('/home/dieu/AMS-outil/cpu_ram.json', 'r') as f:
    cpu_ram = json.load(f)

with open('/home/dieu/AMS-outil/disk.json', 'r') as f:
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
