FROM python:3.11-slim

RUN mkdir -p /project/

RUN pip install --upgrade pip

COPY requirments.txt /project/requirments.txt

RUN pip install --no-cache-dir -r /project/requirments.txt

COPY ../core/ /project/core/

WORKDIR /project/core/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD celery -A antalia_project worker -l info -B