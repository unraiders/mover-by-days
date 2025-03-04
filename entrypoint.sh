#!/bin/sh

if [ -z "$CRON_SCHEDULE" ]; then
    echo "La variable HORA no está definida en el archivo .env"
    exit 1
fi

if [ ! -d "$SOURCE_PATH" ]; then
    echo "El directorio SOURCE_PATH ($SOURCE_PATH) no existe."
    exit 1
fi

if [ ! -d "$DEST_PATH" ]; then
    echo "El directorio DEST_PATH ($DEST_PATH) no existe."
    exit 1
fi

echo "$(date +'%d-%m-%Y %H:%M:%S') $VERSION - Arrancando entrypoint.sh"
echo "$(date +'%d-%m-%Y %H:%M:%S') Antigüedad días a mover: $DAYS_THRESHOLD"
echo "$(date +'%d-%m-%Y %H:%M:%S') Programación cron: $CRON_SCHEDULE"
echo "$(date +'%d-%m-%Y %H:%M:%S') Debug: $DEBUG"
echo "$(date +'%d-%m-%Y %H:%M:%S') Prueba: $PRUEBA"
echo "$(date +'%d-%m-%Y %H:%M:%S') Zona horaria: $TZ"

CRON_JOB="$CRON_SCHEDULE python3 /app/sync_files.py >> /proc/1/fd/1 2>> /proc/1/fd/2"

echo "$CRON_JOB" > /etc/crontabs/root

echo "Arrancando cron..."
crond -f -l 2 || { echo "Error arrancando cron"; exit 1; }