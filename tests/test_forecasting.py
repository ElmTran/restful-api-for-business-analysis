# Standard Library
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Third-Party Libraries
import pandas as pd

# Project Imports
from forecasters import TimeSeriesForecasterCreator

# set working directory

if __name__ == "__main__":
    data = pd.read_csv("attachments/time_series_test.csv")
    params = {
        "features": ["Month"],
        "target": "Ridership",
        "time_format": "%m/%d/%Y",
        "rate": 0.2,
        "random_state": 3,
        "predays": 32,
    }

    forecaster = TimeSeriesForecasterCreator("arima", data, params).create()

    result = forecaster.forecast()
    print(result)
