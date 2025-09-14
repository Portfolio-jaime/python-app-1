FROM python:3.10-alpine

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./src /src
COPY ./templates /src/templates

CMD python /src/app.py

