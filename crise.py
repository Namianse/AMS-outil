import sqlite3
import json

with open('/home/dieu/AMS-outil/config_crise.json', 'r') as f:
    config = json.load(f)

conn = sqlite3.connect('/home/dieu/AMS-outil/monitoring.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM metrics ORDER BY rowid DESC LIMIT 1')
result = cursor.fetchone()

if result is None:
    print("Aucune donnée")
else:
    timestamp, cpu, ram, disque_pct = result

    cpu_alerte    = '/!\\' if cpu > config['seuil_cpu'] else ''
    ram_alerte    = '/!\\' if ram > config['seuil_ram'] else ''
    disque_alerte = '/!\\' if disque_pct > config['seuil_disque'] else ''
    
    cpu_str    = f"CPU : {cpu}% {cpu_alerte}"
    ram_str    = f"RAM : {ram}% {ram_alerte}"
    disque_str = f"Disque : {disque_pct}% {disque_alerte}"

    crise = any([
        cpu > config['seuil_cpu'],
        ram > config['seuil_ram'],
        disque_pct > config['seuil_disque']
    ])

    if crise:
        print("/!\ Crise détectée")
    else:
        print("Aucun problème détectée.")

    print(cpu_str)
    print(ram_str)
    print(disque_str)
