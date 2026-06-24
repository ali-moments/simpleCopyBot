FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv && uv sync

COPY . .

CMD ["uv", "run", "main.py"]