# Third-Party Libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from .base import BaseForecaster, BaseForecasterCreator


class SentimentAnalysisForecaster(BaseForecaster):
    def __init__(self):
        super().__init__()
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()

    def split_data(self):
        rate = self.params.get("rate", 0.2)
        ramdom_state = self.params.get("random_state", 0)
        (
            self.x_train,
            self.x_test,
            self.y_train,
            self.y_test,
        ) = train_test_split(
            self.data[self.features],
            self.data[self.target],
            test_size=rate,
            random_state=ramdom_state,
        )

    def fit(self):
        self.x_train = self.vectorizer.fit_transform(self.x_train)
        self.model.fit(self.x_train, self.y_train)

    def predict(self):
        self.x_test = self.vectorizer.transform(self.x_test)
        self.y_pred = self.model.predict(self.x_test)

    def evaluate(self):
        self.accuracy = accuracy_score(self.y_test, self.y_pred)

    def package_results(self) -> dict:
        return {
            "model": self.model,
            "x_train": self.x_train,
            "x_test": self.x_test,
            "y_train": self.y_train,
            "y_test": self.y_test,
            "y_pred": self.y_pred,
            "accuracy": self.accuracy,
        }


# todo: add more forecasters
# NRC
# bing


class SentimentAnalysisForecasterCreator(BaseForecasterCreator):
    forecaster_classes = {
        "sentiment_analysis": SentimentAnalysisForecaster,
    }
