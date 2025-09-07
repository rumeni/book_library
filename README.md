# Book Library REST API

Django REST API for managing books in a library with React frontend.

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework, PostgreSQL 15
- **Frontend**: React 18, CSS3
- **Infrastructure**: Docker, Docker Compose

## Quick Start

### Using Docker (Recommended)

```bash
git clone <repository>
cd book_library
docker-compose up --build
```

**Access:**

- Frontend: http://localhost:3000
- API: http://localhost:8000/books/
- Admin: http://localhost:8000/admin

### Local Development

#### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Copy the example file and update with your values
cp .env.example .env
# Edit .env with your actual configuration values

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Populate sample data (optional)
python manage.py populate_books

# Run server
python manage.py runserver
```

#### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## API Endpoints

| Method   | Endpoint                     | Description                          |
| -------- | ---------------------------- | ------------------------------------ |
| `GET`    | `/books/`                    | List books with filtering and search |
| `POST`   | `/books/`                    | Create new book                      |
| `GET`    | `/books/{id}/`               | Get book details                     |
| `PATCH`  | `/books/{id}/`               | Update book                          |
| `DELETE` | `/books/{id}/`               | Delete book                          |
| `PATCH`  | `/books/update-by-author/`   | Bulk update books by author          |
| `GET`    | `/books/by-author/{author}/` | Get books by author                  |

### Query Parameters

**Search and Filtering:**

```bash
# Search in title and author
GET /books/?search=tolkien

# Filter by genre
GET /books/?genre__icontains=fantasy

# Date range filtering
GET /books/?publication_date_from=2020-01-01&publication_date_to=2023-12-31

# Ordering (case-insensitive for title/author)
GET /books/?ordering=-title
GET /books/?ordering=author
```

**Pagination:**

```bash
GET /books/?page=2
```

## Features

### Backend

- Complete CRUD operations
- Case-insensitive search and sorting
- ISBN validation (ISBN-10/13 format)
- Bulk operations
- Database indexing for performance
- Comprehensive test coverage

### Frontend

- Responsive design
- Real-time search and filtering
- Dark/light theme toggle
- Book form with validation
- Author-based operations

## Database Schema

```sql
CREATE TABLE books_book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) DEFAULT '',
    publication_date DATE,
    description TEXT,
    genre VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_books_author ON books_book(author);
CREATE INDEX idx_books_genre ON books_book(genre);

-- ISBN uniqueness constraint (only for non-empty values)
ALTER TABLE books_book ADD CONSTRAINT unique_non_empty_isbn
UNIQUE (isbn) WHERE isbn != '';
```

## Testing

```bash
# Run all tests
docker-compose exec backend python manage.py test

# Run specific test
python manage.py test books.tests.BookAPITest

# Check test coverage
python manage.py test books.tests -v 2
```

### Troubleshooting Tests

If you encounter PostgreSQL collation version warnings:

```bash
# Stop containers and remove volumes
docker-compose down -v

# Rebuild and restart
docker-compose up --build

# Then run tests
docker-compose exec backend python manage.py test
```

**Note:** PostgreSQL collation warnings are common in Docker environments and don't affect test functionality.

## Project Structure

```
book_library/
├── books/                  # Django app
│   ├── models.py          # Book model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API viewsets
│   ├── filters.py         # Custom filters
│   ├── admin.py           # Admin interface
│   ├── tests.py           # Test cases
│   └── constants.py       # ISBN patterns
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   └── services/      # API services
│   └── public/
├── library/               # Django project settings
├── docker-compose.yml     # Multi-container setup
├── Dockerfile            # Backend container
└── requirements.txt      # Python dependencies
```

## Environment Variables

The application requires environment variables for configuration. Create a `.env` file in the project root with the following variables:

| Variable                 | Description           | Required |
| ------------------------ | --------------------- | -------- |
| `DJANGO_SECRET_KEY`      | Django secret key     | Yes      |
| `DEBUG`                  | Debug mode            | Yes      |
| `ALLOWED_HOSTS`          | Allowed hosts         | Yes      |
| `POSTGRES_DB`            | Database name         | Yes      |
| `POSTGRES_USER`          | Database user         | Yes      |
| `POSTGRES_PASSWORD`      | Database password     | Yes      |
| `POSTGRES_HOST`          | Database host         | Yes      |
| `POSTGRES_PORT`          | Database port         | Yes      |
| `DB_CONN_MAX_AGE`        | DB connection max age | Yes      |
| `PAGE_SIZE`              | API pagination size   | Yes      |
| `CORS_ALLOWED_ORIGINS`   | Allowed CORS origins  | Yes      |
| `CORS_ALLOW_CREDENTIALS` | Allow credentials     | Yes      |
| `CORS_ALLOW_ALL_ORIGINS` | Allow all origins     | Yes      |

**Note:** Use the provided `.env.example` as a template. Copy it to `.env` and update with your actual configuration values.

## Development Commands

```bash
# Django commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py shell

# Docker commands
docker-compose up -d          # Run in background
docker-compose logs backend   # View backend logs
docker-compose restart backend
docker-compose down           # Stop all services

# Populate sample data
docker-compose exec backend python manage.py populate_books

# Database access
docker exec -it book_library_db psql -U postgres -d book_library
```
