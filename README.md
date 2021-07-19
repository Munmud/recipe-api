# recipe-api
Recipe app api source code

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
```

`docker build .`

### docker-compose.yml
---
```
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
```
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