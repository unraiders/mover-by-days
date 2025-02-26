FROM python:3.12-alpine

LABEL maintainer="unraiders"
LABEL description="Ejecutar rsync con días de antigüedad, teniendo en cuenta hardlinks y pausar/reanudar los torrents sedeados en qBittorrent."

ARG VERSION=1.0.1
ENV VERSION=${VERSION}

# Instalar cron y otros paquetes
RUN apk add --no-cache dcron rsync findutils mc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sync_files.py .
COPY logic_seed.py .

COPY utils.py .

COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]