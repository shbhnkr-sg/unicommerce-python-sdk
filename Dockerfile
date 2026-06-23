FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY unicommerce/ unicommerce/
COPY mcp_server.py .

RUN pip install --no-cache-dir ".[mcp]"

EXPOSE 8000

ENTRYPOINT ["python", "mcp_server.py"]
