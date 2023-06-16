# Third-Party Libraries
import nltk
from langdetect import detect
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Project Imports
from models.task import Attachment
from .base import BaseClassifier, BaseForecasterCreator


class SentimentClassifier(BaseClassifier):
    def __init__(self, data, params):
        if max_features := params.get("max_features", None):
            data = data.sample(max_features)
        super().__init__(data, params)
        self.model = SentimentIntensityAnalyzer()

    def preprocess(self):
        pass

    def process(self):
        # drop no-english comments
        for i, row in self.data.iterrows():
            try:
                if detect(row["comments"]) != "en":
                    self.data.drop(i, inplace=True)
            except Exception:
                self.data.drop(i, inplace=True)

        sentiments = (
            self.data[self.target]
            .apply(
                lambda comment: 1
                if self.model.polarity_scores(comment)["compound"] >= 0
                else 0
            )
            .tolist()
        )
        self.data["sentiment"] = sentiments

    def package_results(self):
        attachment = Attachment.create(
            f"result_{self.params['task_id']}.csv",
            self.data.to_csv(index=False),
        )
        return {
            "model": "vader",
            "attachment_id": attachment._id,
            "success": True,
        }


class SentimentSplitter(BaseClassifier):
    def __init__(self, data, params):
        super().__init__(data, params)
        self.model = SentimentIntensityAnalyzer()
        self.customer_stop_words = params.get("customer_stop_words", None)
        self.stop_words = set(stopwords.words("english"))
        self.words = None

    def preprocess(self):
        words = [word.lower() for word in nltk.word_tokenize(self.data)]
        words = [
            word
            for word in words
            if word not in self.stop_words and word.isalpha() and len(word) > 2
        ]
        if self.customer_stop_words:
            words = [
                word for word in words if word not in self.customer_stop_words
            ]
        self.words = words

    def process(self):
        self.preprocess()
        self.result = {}
        for word in self.words:
            if self.model.polarity_scores(word)["compound"] >= 0:
                self.result[word] = 1
            else:
                self.result[word] = 0

    def package_results(self):
        return self.result


class SentimentAnalyzerCreator(BaseForecasterCreator):
    forecaster_classes = {
        "file": SentimentClassifier,
        "text": SentimentSplitter,
    }
