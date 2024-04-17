FROM python:3.12.0 as builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1 
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.12.0-slim-bullseye as runtime

ENV VIRTUAL_ENV=/.venv
ENV PATH="/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN apt-get update && apt-get install libpq5 -y

COPY alembic.ini ./
COPY alembic ./alembic
COPY url_shortener ./url_shortener
COPY entrypoint.sh ./entrypoint.sh
COPY .env ./.env

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]