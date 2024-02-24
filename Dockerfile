FROM python:3.10.12-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /FastAPI_REF
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . ./