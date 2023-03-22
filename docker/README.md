# Установка и запуск
```bash
 docker-compose up -d
```

# Переменные окружения

Postgres:
- user: `postgres`
- password: `password`
- host_port: `http://localhost:5432/`
- db: `postgres`

PgAdmin:
- user: `admin@admin.ru`
- password: `password`
- host_port: `http://localhost:5050/`

Redis:
- port: `6379`


# Остановка сервисов
```bash
docker-compose stop
```
