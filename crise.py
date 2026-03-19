import sqlite3
import json
import smtplib
import pygal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER  = 'partage.univ-avignon.fr'
SMTP_PORT    = 465
EXPEDITEUR   = 'nathan.serra@alumni.univ-avignon.fr'
DESTINATAIRE = 'nathan.serra@alumni.univ-avignon.fr'

def generer_graphiques(cursor):
    cursor.execute('SELECT timestamp, cpu, ram, disque_pct FROM metrics ORDER BY rowid ASC')
    rows = cursor.fetchall()

    timestamps = [r[0] for r in rows]
    cpu_vals   = [r[1] for r in rows]
    ram_vals   = [r[2] for r in rows]
    disk_vals  = [r[3] for r in rows]

    chart = pygal.Line(x_label_rotation=45)
    chart.title = 'Monitoring'
    chart.x_labels = timestamps
    chart.add('CPU (%)',    cpu_vals)
    chart.add('RAM (%)',    ram_vals)
    chart.add('Disque (%)', disk_vals)

    fichier = '/home/dieu/AMS-outil/graph_monitoring.svg'
    chart.render_to_file(fichier)

    return [fichier]

def envoyer_mail(cpu_str, ram_str, disque_str, timestamp, fichiers):
    with open('/home/dieu/AMS-outil/mail_template.txt', 'r') as f:
        template = f.read()

    contenu_formate = template.format(
        cpu_str=cpu_str,
        ram_str=ram_str,
        disque_str=disque_str,
        timestamp=timestamp
    )

    lignes  = contenu_formate.split('\n')
    sujet   = lignes[0].replace('SUJET: ', '')
    contenu = '\n'.join(lignes[2:])

    msg = MIMEMultipart()
    msg['Subject'] = sujet
    msg['From']    = EXPEDITEUR
    msg['To']      = DESTINATAIRE
    msg.attach(MIMEText(contenu))

    for fichier in fichiers:
        with open(fichier, 'rb') as f:
            partie = MIMEBase('application', 'octet-stream')
            partie.set_payload(f.read())
            encoders.encode_base64(partie)
            partie.add_header('Content-Disposition', f'attachment; filename="{fichier.split("/")[-1]}"')
            msg.attach(partie)

    with open('/home/dieu/AMS-outil/mdp_mail.txt', 'r') as f:
        MOT_DE_PASSE = f.read().strip()

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
        fichiers = generer_graphiques(cursor)
        envoyer_mail(cpu_str, ram_str, disque_str, timestamp, fichiers)
    else:
        print("Aucun problème détecté.")

    print(cpu_str)
    print(ram_str)
    print(disque_str)
