# ToDo List test project

<!-- TOC -->
* [ToDo List test project](#todo-list-test-project)
  * [Описание](#описание)
  * [Стек](#стек)
  * [Компоненты](#компоненты)
    * [Взаимодействие компонентов](#взаимодействие-компонентов)
  * [Как запустить](#как-запустить)
    * [Переменные окружения](#переменные-окружения)
    * [Docker](#docker)
    * [Создание суперпользователя](#создание-суперпользователя)
<!-- TOC -->

## Описание

Бот Telegram, который позволяет выполнять CRUD над задачами ToDo и их категориями, 
а также бот может уведомлять вас о завершении задачи.

## Стек

Bot:
- aiogram3
- aiogram-dialog

Backend:
- Django 5 + DRF 3
- Celery + Redis
- PostgreSQL

## Компоненты

1. Django (backend)
- Обрабатывает REST API-запросы от Telegram-бота.
- Управляет пользователями, задачами и напоминаниями.
- Работает через `gunicorn`.
- Использует PostgreSQL для хранения данных.
- Отправляет фоновые задачи в Celery.

2. Telegram-бот
- Построен на `aiogram` / `aiogram_dialog`.
- Получает команды от пользователя.
- Обращается к Django API для получения и отправки данных.

3. Celery
- Обрабатывает фоновые задачи (напоминания).
- Использует Redis как брокер сообщений.
- Работает с Django-моделями (через общий код/базу данных).

4. Redis
- Брокер сообщений для Celery.

5. PostgreSQL
- Основная СУБД.
- Хранит пользователей, задачи, напоминания и пр.


### Взаимодействие компонентов
- Бот обращается к Django через HTTP API.
- Django использует ORM для работы с PostgreSQL.
- Для задач по расписанию — Django → Celery → Redis.
- Celery обновляет данные в PostgreSQL по завершении задач.


## Как запустить

### Переменные окружения

<details>
<summary>Пример</summary>

```
DJANGO_SECRET_KEY=supersecret
DEBUG=False
API_HOST=backend

DB_ENGINE=django.db.backends.postgresql
DB_NAME=todo
DB_USER=root
DB_PASSWORD=Passw0rd12
DB_HOST=postgres
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=Passw0rd12

CELERY_ACCEPT_CONTENT=json
CELERY_TASK_SERIALIZER=json
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

TELEGRAM_BOT_TOKEN=12345678910:dfwf wecwcfe
API_URL=http://backend:8000/api/v1
```

</details>

**Описание:**

```text
DJANGO_SECRET_KEY - секретный ключ Django
DEBUG — режим отладки (логическое значение python)
API_HOST — имя хоста бэкенд-сервиса (пример и т. д.)

DB_ENGINE — тип движка Django (django.db.backends.postgresql, django.db.backends.sqlite3 и т. д.)
DB_NAME — имя БД сервиса
DB_USER — имя пользователя в БД (устанавливается при настройке)
DB_PASSWORD — пароль пользователя в БД (устанавливается при настройке)
DB_HOST - адрес БД
DB_PORT - порт БД

REDIS_HOST - адрес Redis
REDIS_PORT - порт Redis
REDIS_PASSWORD - пароль Redis

CELERY_ACCEPT_CONTENT - контент, принимаемы Celery
CELERY_TASK_SERIALIZER - сериализатор задач Celery
CELERY_TASK_ACKS_LATE - задача подтверждается только после успешного выполнения
CELERY_TASK_REJECT_ON_WORKER_LOST - вернуть задачу обратно в очередь в случае падения

TELEGRAM_BOT_TOKEN - токен Telegram бота
API_URL — URL API бэкенд-сервиса (http://backend:8000/api/v1 и т. д.)
```

### Docker

Запустите следующий docker-compose из корневого каталога `todo_list`.
Не забудьте положить рядом с ним файл **.env**.

```shell
docker-compose up -d --build
```
<details>
<summary>Compose file</summary>

```yaml
version: "3"
services:
  postgres:
    container_name: postgres
    hostname: postgres
    image: postgres
    restart: always
    environment:
      POSTGRES_DB: db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network
  redis:
    image: "redis:latest"
    container_name: redis
    ports:
      - 6379:6379
    command: >
      --requirepass ${REDIS_PASSWORD}
    volumes:
      - ./redis_data:/data
    env_file:
      - ./.env
    networks:
      - app_network
  backend:
    container_name: backend
    hostname: backend
    build: ./backend
    volumes:
      - ./backend:/app
      - ./static:/app/static
    ports:
      - "8000:8000"
    env_file:
      - ./.env
    depends_on:
      - redis
      - postgres
    networks:
      - app_network
  celery:
    build: ./backend
    container_name: celery_worker
    command: celery -A backend.celery worker --loglevel=info
    volumes:
      - ./backend:/app
    depends_on:
      - redis
      - backend
    environment:
      - REDIS_HOST=redis
    env_file:
      - ./.env
    networks:
      - app_network

  bot:
    container_name: todo_bot
    hostname: bot
    build: ./bot
    depends_on:
      - backend
    env_file:
      - ./.env
    networks:
      - app_network

volumes:
  postgres_data:
  static:
    
networks:
  app_network:
    driver: bridge


```

</details>

Или сначала создайте образы сервисов `backend` и `bot` из соответствующих папок, 
а затем добавьте их в образы в compose вместо build.

```shell
docker build -t backend .
```

```shell
docker build -t bot .
```

### Создание суперпользователя

Если вы хотите посетить панель администратора, вам потребуется суперпользователь.

После того, как служба `backend` будет запущена, вы можете использовать следующую 
команду для его создания:

```shell
docker exec -it <container_name> python manage.py createsuperuser
```