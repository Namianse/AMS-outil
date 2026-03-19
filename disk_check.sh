timestamp=$(date +%Y-%m-%dT%H:%M:%S)
pct=$(df --total -h | awk '/^total/ {print $5}' | tr -d '%')
data="{\"timestamp\": \"$timestamp\", \"disque_pct\": $pct}"
echo "$data" > /home/dieu/AMS-outil/disk.json
echo "$data"
