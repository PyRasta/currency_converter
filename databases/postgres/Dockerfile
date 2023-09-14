FROM postgres:latest

ENV POSTGRES_DB rates
ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword

COPY init.sql /docker-entrypoint-initdb.d/