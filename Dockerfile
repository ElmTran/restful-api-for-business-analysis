# Build Stage
FROM python:3.8-alpine AS builder

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev \
    && python -m venv /venv \
    && /venv/bin/pip install --no-cache-dir --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps gcc musl-dev libffi-dev openssl-dev

# Final Stage
FROM python:3.8-alpine

# Create a non-root user
RUN adduser -D myuser

# Switch to non-root user
USER myuser

# Set work directory
WORKDIR /usr/src/app

# Copy dependencies from builder stage
COPY --from=builder /venv /usr/src/app/venv
COPY --from=builder /usr/src/app .

# Copy project
COPY . .

# Expose the port server is running on
EXPOSE 8976

# Activate virtual environment
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Start server
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8976 analyzer.wsgi && python celery_main.py"]
