# FastAPI Todo Application

A simple Todo application built for learning and practicing modern Backend development with FastAPI.

The project demonstrates:

* REST API development with FastAPI
* Authentication with JWT
* PostgreSQL integration
* SQLAlchemy ORM
* Alembic database migrations
* Docker & Docker Compose
* Jinja2 templates
* HTML / CSS / JavaScript frontend

---

## Technologies

* Python 3.13
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Docker
* Docker Compose
* Jinja2
* HTML
* CSS
* JavaScript

---

## Project Structure

```text
FastAPI/
│
├── TodoApp/
│   ├── routers/
│   ├── templates/
│   ├── static/
│   ├── alembic/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Prerequisites

Make sure you have installed:

* Docker Desktop
* Git

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Move into the project

```bash
cd FastAPI
```

### 3. Create the environment file

Create a `.env` file based on `.env.example`.

Example:

```env
POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

DATABASE_URL=postgresql://your_username:your_password@db:5432/your_database

SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

---

## Run the project

Build and start the containers:

```bash
docker compose up --build
```

---

## API Documentation

Swagger UI:

```
http://localhost:8000/docs
```

Application:

```
http://localhost:8000
```

---

## Stop the project

```bash
docker compose down
```

---

## Remove containers and database volume

```bash
docker compose down -v
```

---

## Notes

* PostgreSQL runs inside a Docker container.
* Database data is stored using a Docker volume.
* Sensitive information is stored in `.env` and is **not** committed to Git.
* `.env.example` is provided as a template for configuration.
