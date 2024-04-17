#!/bin/sh

alembic upgrade heads
uvicorn url_shortener_auth.web.app:app --host 0.0.0.0 --port 8001 --reload