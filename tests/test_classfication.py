# Standard Library
import os
import sys

# Third-Party Libraries
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Project Imports
from forecasters import ClassifierCreator

if __name__ == "__main__":
    data = pd.read_csv("attachments/classification_test.csv")
    params = {
        "excludes": [],
        "dummies": [
            "abtest",
            "vehicleType",
            "gearbox",
            "fuelType",
            "brand",
            "notRepairedDamage",
        ],
        "target": "good_sale",
        "max_features": 100,
    }

    tester = ClassifierCreator("log_regression", data, params).create()
    print(tester.forecast())
