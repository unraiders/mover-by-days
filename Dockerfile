FROM python:3.12-alpine

LABEL maintainer="unraiders"
LABEL description="Ejecutar rsync con días de antigüedad y teniendo en cuenta hardlinks"

ARG VERSION=1.0.0
ENV VERSION=${VERSION}

# Instalar cron y otros paquetes
RUN apk add --no-cache dcron rsync findutils mc

WORKDIR /app

COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sync_files.py .
COPY logic_seed.py .

COPY utils.py .

ENTRYPOINT ["/app/entrypoint.sh"]