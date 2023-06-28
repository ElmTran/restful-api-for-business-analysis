# Use an official Python runtime as a parent image
FROM python:3.8-alpine AS build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

###################
# FINAL IMAGE
###################
FROM python:3.8-alpine

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /home/appuser

# Install dependencies
COPY --from=build /usr/src/app/wheels /wheels
COPY --from=build /usr/src/app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy project
COPY . .

# Change the ownership of the application directory to the non-root user
RUN chown -R appuser:appgroup /home/appuser

# Switch to the non-root user
USER appuser

# Expose the port server is running on
EXPOSE 8000

# Start server
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8000 analyzer.wsgi && python celery_main.py"]