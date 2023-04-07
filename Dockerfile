FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -U setuptools pip && pip3 install -r requirements.txt

