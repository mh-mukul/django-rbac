# Django RBAC Project

A Django REST Framework project with Role-Based Access Control (RBAC).

## Features

- Custom User model with email-based authentication
- Role-based access control (RBAC)
- JWT authentication using djangorestframework-simplejwt
- Modular project structure
- Environment-specific settings
- Docker support

## Project Structure

```
project_name/
├── config/                     # Main project config (settings, urls, wsgi, asgi)
│   ├── __init__.py
│   ├── settings/               # Split settings for better management
│   │   ├── __init__.py
│   │   ├── base.py             # Base settings shared by all environments
│   │   ├── dev.py              # Development settings
│   │   ├── prod.py             # Production settings
│   │   ├── staging.py          # Staging settings
│   ├── urls.py                 # Root URL config
│   ├── asgi.py
│   ├── wsgi.py
│
├── apps/                       # Custom apps go here (modular structure)
│   ├── __init__.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── permissions.py
│   │   └── services.py         # Business logic
│   │
│   ├── core/                   # Core utilities / shared app
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── utils.py
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   └── mixins.py
│
├── requirements/               # Dependency management
│   ├── base.txt
│   ├── dev.txt
│   ├── prod.txt
│
├── scripts/                    # Deployment/utility scripts
│   ├── entrypoint.sh
│   ├── init_db.sh
│   └── backup_db.sh
│
├── .env.example                # Example env variables
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── README.md
```

## Setup

### Development Setup

1. Clone the repository:

```
git clone https://github.com/yourusername/django-rbac.git
cd django-rbac
```

2. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```
pip install -r requirements/dev.txt
```

4. Create a `.env` file:

```
cp .env.example .env
```

5. Apply migrations:

```
python manage.py migrate
```

6. Create a superuser:

```
python manage.py createsuperuser
```

7. Run the development server:

```
python manage.py runserver
```

### Docker Setup

1. Make sure you have Docker and Docker Compose installed

2. Build and run the containers:

```
docker-compose up -d --build
```

3. Access the application at http://localhost:8000

## API Documentation

API endpoints:

- `/api/v1/users/` - User management
- `/api/v1/users/roles/` - Role management
- `/api/v1/users/permissions/` - Permission management

## License

This project is licensed under the MIT License - see the LICENSE file for details.
