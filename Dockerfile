FROM python:3.9

RUN pip install django djangorestframework pytest pytest-django
WORKDIR /code