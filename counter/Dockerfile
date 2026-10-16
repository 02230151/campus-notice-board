FROM python:3.12-alpine

ARG VERSION=1.0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN adduser -D appuser

USER appuser

ENV APP_VERSION=${VERSION}

LABEL org.opencontainers.image.title="Campus Notice Board Counter"
LABEL org.opencontainers.image.description="View counter service"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.authors="Tashi D Rinzin"

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')"

CMD ["python", "app.py"]