FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc


COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM python:3.11-slim

RUN addgroup --system app && adduser --system --group app
USER app

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY robbot/ robbot/

ENTRYPOINT ["python", "-m", "robbot"]