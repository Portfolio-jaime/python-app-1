FROM python:3.10-alpine

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

RUN apk add --no-cache sudo

RUN addgroup -g 1001 -S arheanja && \
    adduser -S arheanja -G arheanja -u 1001 && \
    echo "arheanja ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir -p /app/data && \
    chown -R arheanja:arheanja /app

COPY --chown=arheanja:arheanja ./src /app/src

USER arheanja

WORKDIR /app

CMD python /app/src/app.py

