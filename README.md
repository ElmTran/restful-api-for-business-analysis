# RESTful API for Business Analytics
## Introduction

This is a RESTful API for Business Analytics. It is built with Python, Django, Celery, and MySQL. 

## Features

- User authentication
- User authorization
- File upload
- Time series forecasting
- Classification
- Clustering
- Sentiment analysis
- Result download

## Installation

### Prerequisites

- Python 3.8.10
- MySQL 5.7.18
- RabbitMQ 3.12.0

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
    python manage.py runserver && python celery_main.py
    ```

### Docker

1. From Docker Hub

    ```bash
    docker pull elmtran/analysis-api
    ```

2. Or from source

    ```bash
    git clone https://github.com/ElmTran/restful-api-for-business-analysis

    cd restful-api-for-business-analysis

    docker build -t analysis-api .
    ```

3. Run the server

    ```bash
    docker run -p 8976:8976 -v /path/to/.env.prod:/usr/src/app/settings/.env.prod analysis-api -d
    ```
#### Compose

1. Yaml file

    ```yaml
    version: "3.9"
    services:
    analysis-api:
        image: elmtran/analysis-api
        restart: always
        ports:
        - "8976:8976"
        volumes:
        - /path/to/.env.prod:/usr/src/app/settings/.env.prod
    ```
2. Run

    ```bash
    docker-compose up -d
    ```

## Usage

### API Endpoints

1. Register: **POST** /user/register

    ```json
    {
        "username": string,
        "password": string,
        "email": string
    }
    ```

2. Login: **POST** /api/v1/login

    ```json
    {
        "username": string,
        "password": string
    }
    ```

3. Upload: **POST** /api/v1/upload

    authorization: Token {token}

    ```form
    "file": file
    ```

4. Create Task: **POST** /api/v1/create

    authorization: Token {token}

    ```json
    "attachment_id": int,
    "title": string,
    "description": string,
    "category": choice[0, 1, 2, 3],
    "params": object
    ```

5. Query Result: **GET** /api/v1/result/{task_id}

    authorization: Token {token}

6. Download Result: **GET** /api/v1/download/{task_id}

    authorization: Token {token}

### Categories and Parameters

- Time series forecasting: 0

    ```json
    {
        "method": choice[
            "linear_regression",
            "move_average",
            "lstm",
            "simple_exponential_smoothing",
            "holt",
            "holt_winters_seasonal",
            "arima"
        ],                      // the model to be used for forecasting
        "features": list[string],   // the features to be used for forecasting
        "target": string,        // the target to be forecasted
        "max_features": int,    // sample size
        "time_format": string,   // the format of the time column
        "rate": float,           // the rate of the test set
        "random_state": int,     // the random state
        "predays": int,          // the number of days to be forecasted into the future
    }
    ```

- Classification: 1

    ```json
    {
        "method": choice[
            "decision_tree",
            "naive_bayes",
            "random_forest",
            "knn",
            "svm",
            "log_regression"
        ],
        "excludes": list[string],  // the features to be excluded
        "dummies": list[string],   // the features need to be dummied
        "target": string,          // the target to be classified
        "max_features": int,       // sample size
    }

- Clustering: 2

    ```json
    {
        "method": choice[
            "kmeans",
            "hierarchical",
            "spectral",
            "dbscan",
            "gaussian_mixture"
        ],
        "features": list[string],  // the features to be used for clustering
        "n_clusters": int,         // the number of clusters
        "random_state": int,       // the random state
    }
    ```

- Sentiment analysis: 3

    ```json
    {
        "method": choice[
            "file",     // analyze the sentiment of a file
            "text"      // analyze the sentiment of a text
        ],
        "target": string,          // the target to be analyzed
        "max_features": int,       // sample size
        "text": string,            // the text to be analyzed (if method is text)
    }
    ```

### Examples

See [examples](https://github.com/ElmTran/restful-api-for-business-analysis/blob/master/apps/apis/tests.py).

## License

The system is available as open source under the terms of the
[MIT License](https://github.com/ElmTran/restful-api-for-business-analysis/blob/master/LICENSE).

