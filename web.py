
from flask import Flask, render_template
import sqlite3
import pygal

app = Flask(__name__)

DB = '/home/dieu/AMS-outil/monitoring.db'

def get_data(hostname):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, cpu, ram, disque_pct FROM metrics WHERE hostname = ? ORDER BY rowid ASC', (hostname,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def generer_graphique(hostname):
    rows = get_data(hostname)
    timestamps = [r[0] for r in rows]
    cpu_vals = [r[1] for r in rows]
    ram_vals = [r[2] for r in rows]
    disk_vals = [r[3] for r in rows]

    chart = pygal.Line(x_label_rotation=45)
    chart.title = f'Monitoring - {hostname}'
    chart.x_labels = timestamps
    chart.add('CPU (%)', cpu_vals)
    chart.add('RAM (%)', ram_vals)
    chart.add('Disque (%)', disk_vals)

    return chart.render_data_uri()

@app.route('/')
def index():
    graph_vm = generer_graphique('VM')
    graph_physique = generer_graphique('MP')
    return render_template('index.html', graph_vm=graph_vm, graph_physique=graph_physique)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
