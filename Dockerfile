FROM python:3.11-slim

RUN mkdir -p /project/

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY ../core/requirments.txt /project/requirments.txt

RUN pip install --no-cache-dir -r /project/requirments.txt

COPY core /project/core/

WORKDIR /project/core/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000