# syntax=docker/dockerfile:1.7

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FATECAT_RUNTIME_ROOT=/app \
    FATE_SERVICE_HOST=0.0.0.0 \
    FATE_SERVICE_PORT=7860 \
    FATE_RECORDS_ENABLED=0 \
    FATE_REQUEST_TIMEOUT_SECONDS=120 \
    FATE_RATE_LIMIT_PER_MINUTE=30 \
    FATE_MAX_INFLIGHT_CALCULATIONS=1 \
    FATE_REPORT_JOB_QUEUE_SIZE=20 \
    FATE_REPORT_JOB_WORKERS=1 \
    FATE_REPORT_JOB_TTL_SECONDS=1800 \
    FATE_TELEGRAM_WEBHOOK_ENABLED=0 \
    FATE_TELEGRAM_WEBHOOK_QUEUE_SIZE=20 \
    FATE_TELEGRAM_WEBHOOK_DEDUPE_SIZE=2048 \
    FATE_TELEGRAM_WEBHOOK_MAX_CONNECTIONS=4 \
    FATE_DEPLOYMENT_REPLICAS=1 \
    FATE_RATE_LIMIT_BACKEND=memory \
    FATE_EDGE_BODY_LIMIT_ENABLED=1 \
    FATE_TRUST_PROXY_HEADERS=1 \
    FATE_ENABLE_HSTS=1 \
    HOME=/tmp \
    NPM_CONFIG_CACHE=/tmp/fatecat-npm-cache \
    PYTHONPATH=/app/domains/fate-analysis/services/fate-core/src:/app/domains/experience-delivery/services/fatecat-delivery/src

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      bash \
      ca-certificates \
      curl \
      nodejs \
      npm \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system fatecat \
    && useradd --system --gid fatecat --home-dir /app --shell /usr/sbin/nologin fatecat

COPY requirements.txt requirements.lock.txt ./

RUN python -m pip install -c requirements.lock.txt --upgrade pip setuptools wheel \
    && python -m pip install -c requirements.lock.txt -r requirements.txt

COPY --chown=fatecat:fatecat . .
COPY infra/docker/entrypoint.delivery.sh /usr/local/bin/fatecat-delivery

RUN chmod +x /usr/local/bin/fatecat-delivery \
    && mkdir -p /app/infra/runtime/local-state/database/bazi /app/infra/runtime/local-state/vendor-build /tmp/fatecat-npm-cache \
    && chown -R fatecat:fatecat /app/infra/runtime/local-state /tmp/fatecat-npm-cache

USER fatecat

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"FATE_SERVICE_PORT\", \"7860\")}/ready', timeout=3).read()"

CMD ["fatecat-delivery"]
