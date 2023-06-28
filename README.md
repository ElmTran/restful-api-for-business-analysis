# RESTful API for Business Analytics
## Introduction

This is a RESTful API for Business Analytics. It is built with Python and Django. It is a part of the project for the course Business Analytics at the Trinity College Dublin.

## Features(Pending)

## Installation

### Prerequisites

- Python 3.8.10
- Django 3.2.12 & Django Rest Framework 3.14.0
- MySQL 5.7.18
- RabbitMQ 3.12.0
- Celery 5.2.7

### Build from source

1. Clone the repository

```bash
git clone https://github.com/ElmTran/restful-api-for-business-analysis

cd restful-api-for-business-analysis
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Set up the settings.py file

```bash
cp settings/.env.template settings/.env.dev

vim settings/.env.dev
```

4. Run the server

```bash
python manage.py runserver

python celery_main.py
```

### Docker(Pending)

## Usage(Pending)

### API Endpoints



