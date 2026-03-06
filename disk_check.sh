df --total -h | awk '/^total/ {print "Espace disque disponible : " $4 "\nEspace disque utilisé : " $3 ", " $5}'
