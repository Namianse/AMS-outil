timestamp=$(date +%Y-%m-%dT%H:%M:%S)
pct=$(df --total -h | awk '/^total/ {print $5}' | tr -d '%')

echo "{\"timestamp\": \"$timestamp\", \"disque_pct\": $pct}" > disk.json
