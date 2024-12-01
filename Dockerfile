FROM python:3.12-alpine AS production

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

COPY requirements/prod.txt ./requirements/prod.txt

RUN python3 -m venv /app/venv

RUN /app/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements/prod.txt

COPY ./bot ./bot

FROM python:3.12-alpine

WORKDIR /app

COPY --from=production /app/venv /app/venv
COPY --from=production /app/bot /app/bot

ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "./bot"]
