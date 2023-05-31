# Standard Library
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Third-Party Libraries
import pandas as pd

# Project Imports
from forecasters import SentimentAnalyzerCreator

if __name__ == "__main__":
    data = pd.read_csv("attachments/sentiment_test.csv")
    params = {
        "target": "comments",
        "max_features": 100,
    }
    # text = "I love this product. It is so good. I hate this product. It is so bad."

    tester = SentimentAnalyzerCreator("file", data, params).create()
    # tester = SentimentAnalyzerCreator("text", text, {}).create()
    result = tester.classify()
    print(result)
