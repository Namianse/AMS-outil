import sqlite3
import json
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER  = 'partage.univ-avignon.fr'
SMTP_PORT    = 465
EXPEDITEUR   = 'nathan.serra@alumni.univ-avignon.fr'
DESTINATAIRE = 'nathan.serra@alumni.univ-avignon.fr'
MOT_DE_PASSE = 'Nathan@29092006!'

def envoyer_mail(cpu_str, ram_str, disque_str, timestamp):
    with open('/home/dieu/AMS-outil/mail_template.txt', 'r') as f:
        template = f.read()
    contenu = template.format(
        cpu_str=cpu_str,
        ram_str=ram_str,
        disque_str=disque_str,
        timestamp=timestamp
    )
    msg = MIMEText(contenu)
    msg['Subject'] = 'ALERTE - Situation de crise détectée'
    msg['From']    = EXPEDITEUR
    msg['To']      = DESTINATAIRE
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EXPEDITEUR, MOT_DE_PASSE)
        smtp.send_message(msg)
        print("Mail envoyé")

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
        print("/!\\ Crise détectée")
        envoyer_mail(cpu_str, ram_str, disque_str, timestamp)
    else:
        print("Aucun problème détecté.")

    print(cpu_str)
    print(ram_str)
    print(disque_str)
