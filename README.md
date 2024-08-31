# Сервис заметок на FastAPI

Этот проект представляет собой REST API сервис для управления заметками, построенный на FastAPI. В проекте реализована аутентификация через HTTP Basic Auth, а данные хранятся в базе данных PostgreSQL. Приложение контейнеризировано с помощью Docker.

## Возможности

- **FastAPI** для создания REST API.
- **PostgreSQL** для хранения данных пользователей и заметок.
- **HTTP Basic Authentication** для защиты доступа к API.
- **Docker** для контейнеризации приложения.
- **Поддержка асинхронных операций** для эффективной обработки запросов.

## Предварительные требования

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2. Создайте файл `.env` в корневой директории проекта по аналогии с файлом `.env_example`


3. Постройте и запустите контейнеры:

    ```sh
    docker-compose up --build
    ```

4. Приложение будет доступно по адресу `http://localhost:8000`.

## Использование

### Конечные точки (Endpoints)

- **POST /notes/**: Создание новой заметки.
- **GET /notes/**: Получение всех заметок для аутентифицированного пользователя.

### Предустановленные пользователи
В сервисе уже есть следующие предустановленные пользователи:

user1 / password1

user2 / password2

## Запуск тестов
Вы можете использовать Postman тестирования API. В репозитории включен файл коллекции Postman (postman_collection.json) для упрощения тестирования. Просто импортируйте его в Postman.

Также можно использовать Swagger UI для тестирования API:

Откройте http://localhost:8000/docs в браузере.