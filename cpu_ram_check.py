import psutil
import time
import datetime

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(f"CPU : {cpu}%")
print(f"RAM : {ram.percent}% utilisée ({round(ram.used / 1024**3, 1)} Go / {round(ram.total / 1024**3, 1)} Go)")
