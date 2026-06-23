FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY unicommerce/ unicommerce/
COPY mcp_server.py .

RUN pip install --no-cache-dir ".[mcp]"

ENTRYPOINT ["python", "mcp_server.py"]
