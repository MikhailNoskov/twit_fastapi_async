# Python advanced diploma project (SkillBox)

## Project structure
* **frontend** - Client part with nginx config
* **backend** - Server part
* **readme.md** - project description
* **docker-compose.yml** - project start up config file 
* **example.env** - environment variables sample file

## Application structure
* **/alembic** - alembic settings and migrations
* **/auth** - oauth2 user authentication
* **/aws** - aws s3 bucket connection for image files upload
* **/database** - db connection settings and crud for users, tweets and media
* **/exception** - custom exceptions
* **/images** - locally stored images
* **/logs** - log files
* **/models** - user, tweet and media models
* **/routes** - endpoints
* **/schema** - request and response schemas for user, tweet, media, etc.
* **/tests** - tests
* **alembic.ini** - alembic settings
* **celery_app.py** - celery config and tasks
* **Dockerfile** - docker file for backend containerization
* **logging_conf.py** - logging config file
* **main.py** - main file with application
* **pyproject,toml, tox.ini** - linters config
* **requirements.txt** - dependencies file
* **settings.py** - projects settings file

## Technologies used
* **Main app**: FastApi, SqlAlchemy, Pydantic, Starlette, Uvicorn
* **Async tasks**: Celery, Redis
* **Database**: Postgresql with asyncpg connection driver, Alembic migrations
* **Containerization**: Docker, DockerCompose
* **Image files handling and AWS storage**: Pillow, boto3
* **Admin page**: fastapi_amis_admin
* **Linters**: black, flake8, mypy
* **Tests**: Pytest
* **User authentication**: Jose, bcrypt, passlib
* **Debugging**: Sentry.

## Containers commands:
```shell
docker-compose up -d --build - start up project as daemon
```
```shell
docker-compose up --build - start up project
```
```shell
docker-compose down - stop project
```
```shell
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit - run tests
```
```shell
docker-compose logs [container name(s)] - get container(s) logs
```