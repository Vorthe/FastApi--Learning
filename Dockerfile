FROM python:3.13-slim

WORKDIR /app

COPY TodoApp/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "cd TodoApp && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]