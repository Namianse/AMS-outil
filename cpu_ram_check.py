import psutil
import time

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    print(f"CPU : {cpu}%")
    print(f"RAM : {ram.percent}% utilisée ({round(ram.used / 1024**3, 1)} Go / {round(ram.total / 1024**3, 1)} Go)")
    time.sleep(3)
