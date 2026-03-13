import urllib.request
import xml.etree.ElementTree as ET
import sqlite3
import datetime
import json

conn = sqlite3.connect('/home/dieu/AMS-outil/monitoring.db')
cursor = conn.cursor()

# Création table Alertes si non existante
cursor.execute('''CREATE TABLE IF NOT EXISTS alertes
              (titre TEXT, lien TEXT)''')
conn.commit()

response = urllib.request.urlopen('https://www.cert.ssi.gouv.fr/alerte/feed/')
root = ET.parse(response).getroot()

# On prend le dernier item (Donc alerte la plus récente
items = root.findall('.//item')
item  = items[-1]
titre = item.find('title').text.strip()
lien  = item.find('link').text.strip()

# S'il y a déjà une entrée avec ce lien, on ajoute pas
cursor.execute('SELECT 1 FROM alertes WHERE lien = ?', (lien,))
if cursor.fetchone() is None:
    cursor.execute('INSERT INTO alertes VALUES (?, ?)', (titre, lien))
    conn.commit()
    print(f"Nouvelle alerte : {titre}")

# Création table Metrics si non existante
cursor.execute('''CREATE TABLE IF NOT EXISTS metrics 
              (timestamp TEXT, cpu REAL, ram REAL, disque_pct REAL)''')
conn.commit()

# On charge les info cpu/rum
with open('/home/dieu/AMS-outil/cpu_ram.json', 'r') as f:
    cpu_ram = json.load(f)

# On charge les info du disque
with open('/home/dieu/AMS-outil/disk.json', 'r') as f:
    disque = json.load(f)

# Fonction qui supprime toute les entrées plus vieilles que 24h
def clean():
    limite = datetime.datetime.now() - datetime.timedelta(hours=24)
    cursor.execute('DELETE FROM metrics WHERE timestamp < ?', (limite.isoformat(),))
    conn.commit()

# Fonction qui insère les données reçues dans la BDD avec la date
def insert():
    cursor.execute('INSERT INTO metrics VALUES (?, ?, ?, ?)', (
        cpu_ram['timestamp'],
        cpu_ram['cpu'],
        cpu_ram['ram'],
        disque['disque_pct']
    ))
    conn.commit()

# On nettoie la table puis on insert

clean()
insert()
