# PrintPro API - Deployment Guide

This guide covers deploying the PrintPro API to production environments.

## 🚀 Deployment Checklist

### Pre-Deployment

- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up proper CORS origins
- [ ] Configure email backend
- [ ] Set up static/media file serving
- [ ] Enable HTTPS
- [ ] Configure database backups
- [ ] Set up monitoring and logging

## 🔧 Environment Setup

### 1. Production Settings

Create a `.env` file:

```env
# Security
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/printpro_production

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# AWS S3 (for media files)
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### 2. Update Settings for Production

Update `config/settings.py`:

```python
from decouple import config
import dj_database_url

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "config.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=printpro_db
      - POSTGRES_USER=printpro_user
      - POSTGRES_PASSWORD=secure_password
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## 🌐 Nginx Configuration

Create `nginx.conf`:

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    client_max_body_size 20M;
}
```

## 🔐 SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal is set up automatically
```

## 🗄️ Database Setup

### PostgreSQL Installation

```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql

CREATE DATABASE printpro_production;
CREATE USER printpro_user WITH PASSWORD 'secure_password';
ALTER ROLE printpro_user SET client_encoding TO 'utf8';
ALTER ROLE printpro_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE printpro_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE printpro_production TO printpro_user;
\q
```

### Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## 📦 Gunicorn Setup

Install Gunicorn:

```bash
pip install gunicorn
```

Create `gunicorn_config.py`:

```python
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
```

Run with:

```bash
gunicorn -c gunicorn_config.py config.wsgi:application
```

## 🔄 Systemd Service

Create `/etc/systemd/system/printpro-api.service`:

```ini
[Unit]
Description=PrintPro API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/printing-api
Environment="PATH=/var/www/printing-api/venv/bin"
ExecStart=/var/www/printing-api/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/printing-api/printpro.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable printpro-api
sudo systemctl start printpro-api
sudo systemctl status printpro-api
```

## 📊 Monitoring

### Setup Logging

Add to settings.py:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/printpro/django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

## 🔄 Database Backups

### Automated Backup Script

Create `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/printpro"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="printpro_production"
DB_USER="printpro_user"

mkdir -p $BACKUP_DIR

# Backup database
PGPASSWORD=$DB_PASSWORD pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_$TIMESTAMP.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete

echo "Backup completed: db_$TIMESTAMP.sql"
```

Add to crontab for daily backups:

```bash
0 2 * * * /path/to/backup.sh
```

## 🚀 Deployment Commands

```bash
# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart printpro-api
```

## 🔍 Health Check Endpoint

Add to `api/views.py`:

```python
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy', 'timestamp': timezone.now()})
```

Add to `api/urls.py`:

```python
path('health/', health_check, name='health-check'),
```

## 📈 Performance Optimization

### Database Optimization

```python
# settings.py
DATABASES = {
    'default': {
        # ... existing config ...
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Caching

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## 🎯 Post-Deployment

1. Test all API endpoints
2. Verify HTTPS is working
3. Check database connections
4. Test file uploads
5. Verify email sending
6. Monitor logs for errors
7. Set up uptime monitoring
8. Configure backup verification

---

**For questions or issues, contact the development team.**

