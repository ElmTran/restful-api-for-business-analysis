# Base Image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN python -m venv /venv \
    && /venv/bin/pip install --no-cache-dir --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose the port server is running on
EXPOSE 8976

# Activate virtual environment
ENV PATH="/venv/bin:$PATH"

# Start server
CMD ["sh", "scripts/start.sh"]
