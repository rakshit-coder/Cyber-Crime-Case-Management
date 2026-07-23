# Django Backend - Secure Case Connect

## 📋 Project Overview

This is a complete Django backend for Secure Case Connect - a secure cybercrime complaint management system with:

- **Security:** AES-256 encryption, bcrypt password hashing, SHA-256 integrity verification
- **Database:** MySQL for data storage
- **Frontend:** HTML, CSS, Bootstrap 5
- **Email:** SMTP for secure communication

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.9+
- MySQL 8.0+
- pip package manager

### 2. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. MySQL Database Setup

```sql
CREATE DATABASE secure_case_connect;
CREATE USER 'case_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON secure_case_connect.* TO 'case_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Environment Configuration

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
SECRET_KEY=your-generated-secret-key
DEBUG=False  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=secure_case_connect
DB_USER=case_user
DB_PASSWORD=strong_password
DB_HOST=localhost
DB_PORT=3306

# Email (Gmail example)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Encryption
ENCRYPTION_KEY=your-32-character-key-here
```

### 6. Generate Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 7. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser

```bash
python manage.py createsuperuser
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000

## 📁 Project Structure

```
backend/
├── secure_case_connect/     # Main project settings
├── users/                   # User management app
├── complaints/              # Complaint filing app
├── cases/                   # Case management app
├── utils/                   # Security utilities
│   ├── security.py         # Encryption, hashing, integrity
│   └── email_manager.py    # Email notifications
├── templates/              # HTML templates
│   ├── auth/              # Login/register
│   ├── dashboard/         # Dashboard pages
│   ├── complaints/        # Complaint pages
│   ├── cases/            # Case pages
│   └── emails/           # Email templates
├── static/                # CSS, JS, images
│   ├── css/
│   └── js/
├── media/                 # User uploads
│   └── evidence/         # Case evidence files
└── manage.py
```

## 🔐 Security Features

### 1. Password Hashing (bcrypt)

```python
from utils.security import PasswordManager

# Hash password
hashed = PasswordManager.hash_password("password123")

# Verify password
is_valid = PasswordManager.verify_password("password123", hashed)
```

### 2. Data Encryption (AES-256)

```python
from utils.security import EncryptionManager

# Encrypt
encrypted = EncryptionManager.encrypt_data("sensitive data")

# Decrypt
plaintext = EncryptionManager.decrypt_data(encrypted)
```

### 3. Integrity Verification (SHA-256)

```python
from utils.security import IntegrityManager

# Calculate hash
hash_value = IntegrityManager.calculate_hash("data")

# Verify hash
is_valid = IntegrityManager.verify_hash("data", hash_value)

# File hash
file_hash = IntegrityManager.calculate_file_hash("/path/to/file")
```

## 📧 Email Configuration

### Gmail Setup

1. Enable 2-factor authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password in `.env`

## 👥 User Roles

1. **User (Regular)** - File complaints
2. **Officer** - Investigate cases, add remarks
3. **Admin** - Manage all cases, users, and officers

## 🗄️ Database Models

### Users App
- `CustomUser` - Extended Django user
- `ActivityLog` - Audit trail
- `SessionManagement` - Session tracking

### Complaints App
- `Complaint` - Main complaint case
- `Evidence` - Uploaded files
- `Remark` - Officer comments
- `ComplaintAttachment` - Phone numbers, emails, URLs

### Cases App
- `CaseWorkflow` - Workflow transitions
- `CaseReport` - Investigation reports
- `CaseStatistics` - Dashboard statistics

## 🧪 Testing

```bash
python manage.py test
```

## 🚀 Production Deployment

### Important Security Steps

1. Set `DEBUG=False` in `.env`
2. Update `SECRET_KEY` with a strong random key
3. Set `SECURE_SSL_REDIRECT=True`
4. Set `SESSION_COOKIE_SECURE=True`
5. Set `CSRF_COOKIE_SECURE=True`
6. Use a production-grade database
7. Use a production WSGI server (Gunicorn, uWSGI)
8. Set up SSL certificate (Let's Encrypt)

### Gunicorn Deployment

```bash
pip install gunicorn
gunicorn secure_case_connect.wsgi:application --bind 0.0.0.0:8000
```

### Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/backend/staticfiles/;
    }

    location /media/ {
        alias /path/to/backend/media/;
    }
}
```

## 📚 API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /register/` - User registration
- `GET /logout/` - User logout

### Dashboard
- `GET /dashboard/` - Main dashboard (role-based)

### Complaints
- `GET /api/complaints/` - List complaints
- `POST /api/complaints/new/` - Create complaint
- `GET /api/complaints/<case_number>/` - View complaint details
- `POST /api/complaints/<case_number>/remark/` - Add remark
- `POST /api/complaints/<case_number>/upload/` - Upload evidence

### Cases
- `GET /api/cases/` - List cases (officers/admins only)
- `GET /api/cases/<case_number>/report/` - View case report

## 🐛 Troubleshooting

### MySQL Connection Error

```
django.db.utils.OperationalError: (1045, "Access denied for user...")
```

**Solution:** Check `.env` database credentials

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Email Not Sending

1. Check Gmail App Password
2. Enable "Less secure app access"
3. Check firewall (SMTP port 587)

## 📖 Documentation

- Django: https://docs.djangoproject.com/
- Bootstrap: https://getbootstrap.com/
- MySQL: https://dev.mysql.com/doc/

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Support

For issues or questions, contact the development team.
