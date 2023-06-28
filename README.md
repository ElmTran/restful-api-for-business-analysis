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


## License

The system is available as open source under the terms of the
[MIT License](https://github.com/ElmTran/restful-api-for-business-analysis/blob/master/LICENSE).

    MIT License

    Copyright (c) 2023 ElmTran

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
