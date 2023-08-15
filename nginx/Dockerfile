FROM python:3.11-slim AS server

RUN mkdir -p /project/

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY ./requirments.txt /project/requirments.txt

RUN pip install --no-cache-dir -r /project/requirments.txt

COPY ./core/ /project/core/

WORKDIR /project/core/

RUN python manage.py collectstatic --noinput

FROM nginx:1.25

RUN rm -v /etc/nginx/nginx.conf

ADD ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx

COPY --from=server project/core/backend_static /nginx/static
