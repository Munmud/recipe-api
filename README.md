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

Stop all running containers: `docker stop $(docker ps -a -q)` <br>
Delete all stopped containers: `docker rm $(docker ps -a -q)`


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