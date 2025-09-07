FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run migrations and start server
# Run: čekaj DB -> migrate -> seed -> runserver
CMD ["sh", "-c", "\
  until pg_isready -h ${POSTGRES_HOST:-db} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres}; do \
    echo 'Waiting for Postgres...'; sleep 2; \
  done && \
  echo 'Postgres is up.' && \
  python manage.py migrate --noinput && \
  python manage.py populate_books && \
  python manage.py runserver 0.0.0.0:8000 \
"]

