FROM python:3.11-slim

WORKDIR /usr/src/app/currency_converter

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x start.sh