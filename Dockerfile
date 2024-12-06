FROM python:3.12-alpine AS production

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

COPY requirements/prod.txt ./requirements/prod.txt

RUN python3 -m venv /app/venv

RUN /app/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements/prod.txt

COPY ./locales ./locales
COPY ./bot ./bot

FROM python:3.12-alpine

WORKDIR /app

COPY --from=production /app/locales /app/locales
COPY --from=production /app/venv /app/venv
COPY --from=production /app/bot /app/bot

ENV PATH="/app/venv/bin:$PATH"

CMD ["sh", "-c", "cd /app/bot && /app/venv/bin/alembic upgrade head && cd .. && /app/venv/bin/pybabel compile -d locales && python ./bot"]
