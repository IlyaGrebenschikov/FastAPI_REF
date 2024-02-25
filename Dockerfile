FROM python:3.10.12-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/project
RUN apt update && \
    apt install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install poetry

COPY . .
WORKDIR /usr/src/project/
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi