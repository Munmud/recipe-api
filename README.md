# recipe-api
Recipe app api build log

### Dockerfile
---
```
FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

```
### create app folder

### requirements.txt
---
```
Django>=2.1.3,<2.2.0
djangorestframework>=3.9.0,<3.10.0
flake8>=3.6.0,<3.7.0
```

`docker build .`

### docker-compose.yml
---
```yml
version: "3"

services:
    app:
        build:
            context: .
        ports:
            - "8000:8000"
        volumes:
            - ./app:/app
        command: >
            sh -c "python manage.py runserver 0.0.0.0:8000"
```

`docker-compose build` <br>
`docker-compose run app sh -c "django-admin.py startproject app ."` <br>


### .travis.yml
---
```yml
language: python
python:
  - "3.6"

services: 
  - docker

before_script: pip install docker-compose

script:
  - docker-compose run app sh -c "python manage.py test && flake8"
```

### app/.flake8
---
```
[flake8]
exclude =
    migrations,
    __pycache__,
    manage.py,
    settings.py
```

``docker-compose run app sh -c "python manage.py startapp core" <br>``

### settings.py
---
```python
INSTALLED_APPS[
'core',
]
```

### core.models
---
```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
    PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""

        if not email:
            raise ValueError('Users must have an email Address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and save a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of usernamme"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

```

### settings.py 
---
```python
AUTH_USER_MODEL = 'core.user'
```

`docker-compose run app sh -c "python manage.py makemigrations core"`

### core.admin.py
---
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)

```


### docker-compose.yml
---
```yml
version: "3"

services:
    app:
        build:
            context: .
        ports:
            - "8000:8000"
        volumes:
            - ./app:/app
        command: >
            sh -c "python manage.py wait_for_db &&
                    python manage.py migrate &&
                    python manage.py runserver 0.0.0.0:8000"
        environment: 
            - DB_HOST=db
            - DB_NAME=app
            - DB_USER=postgres
            - DB_PASS=supersecreatpassword
        depends_on: 
            - db

    db:
        image: postgres:10-alpine
        environment: 
            - POSTGRES_DB=app
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=supersecreatpassword
```

### requirements.txt
---
```
Django>=2.1.3,<2.2.0
djangorestframework>=3.9.0,<3.10.0
psycopg2>=2.7.5,<2.8.0
flake8>=3.6.0,<3.7.0
```

### dockerfile
---
```
FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
```

### settings.py
---
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}
```

### core>management>__init__.py,commands>__init__.py,wait_for_db.py
---
```python
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database available"""

    def handle(self, *args, **options):
        self.stdout.write(' waiting for database... ')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(' Database unavailable, waiting 1 sec... ')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))

```

`docker-compose up`