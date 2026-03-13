import psutil
import datetime
import json

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()

data = {
    "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
    "cpu": cpu,
    "ram": ram.percent
}

with open('cpu_ram.json', 'w') as f:
    json.dump(data, f)
