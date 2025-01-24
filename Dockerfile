FROM python:3.10.13 AS base

# Configure volume/workdir
RUN mkdir /code
WORKDIR /code/
COPY pyproject.toml /code/
COPY poetry.lock /code/

FROM base as deps

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED TRUE
ENV PYTHONPATH=/code/:/usr/lib/python3.10.2/site-packages

# Configure volume/workdir
WORKDIR /code/

# Install poetry
RUN pip install --upgrade pip
RUN pip install --no-cache-dir poetry

# Add and install requirements
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

FROM deps

WORKDIR /code/
COPY . /code/

RUN mkdir static
RUN SECRET_KEY=build_random_secret python manage.py collectstatic

# Create a user with UID 1000 and GID 1000
RUN groupadd -g 1000 appgroup && \
    useradd -r -u 1000 -g appgroup appuser
# Switch to this user
USER 1000:1000

# copy project
COPY . .
