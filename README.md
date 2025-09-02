# Django RBAC Project

A Django REST Framework project with Role-Based Access Control (RBAC).

## Features

- Custom User model with mobile & password authentication
- Role-based access control (RBAC)
- JWT authentication using djangorestframework-simplejwt
- Modular project structure
- Environment-specific settings
- Docker support

## Project Structure

```
django-rbac/
├── README.md
├── docker-compose.yml
├── docker-entrypoint.sh
├── Dockerfile
├── gunicorn.conf.py
├── manage.py
├── requirements.txt
├── .dockerignore
├── .env.example
├── apps/
│   ├── __init__.py
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   │       └── __init__.py
│   ├── authorization/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_initial.py
│   │   │   └── __init__.py
│   │   └── views/
│   │       ├── __init__.py
│   │       ├── modules.py
│   │       ├── permissions.py
│   │       └── roles.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── helpers.py
│   │   ├── models.py
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   └── utils.py
│   ├── organization/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   │       ├── 0001_initial.py
│   │       ├── 0002_initial.py
│   │       └── __init__.py
│   └── user/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── services.py
│       ├── tests.py
│       ├── urls.py
│       ├── views.py
│       └── migrations/
│           ├── 0001_initial.py
│           ├── 0002_alter_user_mobile.py
│           └── __init__.py
└── config/
    ├── __init__.py
    ├── asgi.py
    ├── logger.py
    ├── middleware.py
    ├── urls.py
    ├── wsgi.py
    └── settings/
        ├── __init__.py
        ├── base.py
        ├── dev.py
        ├── prod.py
        └── staging.py
```

## Setup

### Development Setup

1. Clone the repository:

```
git clone https://github.com/mh-mukul/django-rbac.git
cd django-rbac
```

2. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```
pip install -r requirements.txt
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

- `/api/v1/organizations/` - Organization management
- `/api/v1/users/` - User management
- `/api/v1/modules/` - Module management
- `/api/v1/permissions/` - Permission management
- `/api/v1/roles/` - Role management

## License

This project is licensed under the MIT License - see the LICENSE file for details.
