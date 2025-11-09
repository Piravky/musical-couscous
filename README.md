# 📚 Books API - FastAPI проект

RESTful API для управления книгами с асинхронной базой данных PostgreSQL.

## 🚀 Быстрый старт

### Предварительные требования

- **Python 3.12+**
- **PostgreSQL 15+** (или Docker)
- **Git**

### 1. Клонирование репозитория

```bash
git clone https://github.com/Piravky/musical-couscous
cd musical-couscous
```

### 2. Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Linux/macOS)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

```bash
cp .env.example .env
nano .env
```

#### Содержимое `.env` файла:

```bash
# Настройки базы данных
DB_HOST=localhost
DB_USER=user
DB_PORT=5432
DB_PASSWORD=password
DB_DATABASE=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
```

### 5. Настройка базы данных

#### Вариант A: PostgreSQL

```bash
# Установка PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Создание базы данных
sudo -u postgres psql
CREATE DATABASE books_db;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE books_db TO user;
\q
```

#### Вариант B: Docker

```bash
# Запуск PostgreSQL в контейнере
docker run -d \
  --name postgres-books \
  -e POSTGRES_DB=books_db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15

# Проверка статуса
docker ps
```

### 6. Запуск миграций

```bash
# Применение миграций
alembic upgrade head

# Или для создания новой миграции
alembic revision --autogenerate -m "Create initial tables"
```

### 7. Запуск приложения

```bash
python app/main.py
```

Приложение будет доступно по адресу: **http://localhost:8000**

## 📖 Документация API

После запуска приложения документация будет доступна по адресам:

- **Swagger UI**: http://localhost:8000/api/docs
  |

## 🔧 API Эндпоинты

### Books API

| Метод    | Эндпоинт                  | Описание                                      |
|----------|---------------------------|-----------------------------------------------|
| `GET`    | `/api/v1/books/`          | Получить список книг с пагинацией и фильтрами |
| `GET`    | `/api/v1/books/{book_id}` | Получить книгу по ID                          |
| `POST`   | `/api/v1/books/`          | Создать новую книгу                           |
| `PATCH`  | `/api/v1/books/{book_id}` | Частично обновить книгу                       |
| `DELETE` | `/api/v1/books/{book_id}` | Удалить книгу                                 |

## 🐳 Docker развертывание

### Сборка образа docker

```bash
# Сборка Docker образа
docker build -t books-api .

# Проверка образа
docker images
```

### Использование готового образа

```bash
# Запуск готового образа
docker run -d \
  --name books-app \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@host:5432/db \
  books-api
```

### Запуск с Docker compose

```bash
# Запуск с PostgreSQL
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d

# Остановка
docker-compose down
```

---

## 🚀 Команды для быстрого старта

```bash
# Клонирование и запуск
git clone https://github.com/Piravky/musical-couscous && cd musical-couscous
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Настройте .env файл
docker run -d --name postgres-books -e POSTGRES_DB=books_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу http://localhost:8000 📚✨