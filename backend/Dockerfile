FROM python:3.8-slim as builder

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt

FROM python:3.8-slim

COPY --from=builder /requirements.txt /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app

COPY ./interview_app  /app/interview_app
COPY ./tests /app/tests
ADD alembic.ini /app/

EXPOSE 8000