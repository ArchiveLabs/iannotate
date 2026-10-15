FROM python:3.11-slim

WORKDIR /app

# Allow a custom PyPI index (e.g. an internal Nexus mirror) and an HTTP(S) proxy
# at build time, for networks without direct PyPI access. Defaults to public PyPI.
ARG PIP_INDEX_URL=https://pypi.org/simple/
ARG HTTP_PROXY
ARG HTTPS_PROXY

COPY requirements.txt .
RUN pip install --no-cache-dir --index-url "${PIP_INDEX_URL}" -r requirements.txt

COPY app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
