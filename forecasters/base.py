# Standard Library
from abc import ABC, abstractmethod


class BaseForecaster(ABC):
    def __init__(self, data, params):
        self.data = data
        self.params = params
        self.model = None
        self.features = params.get("features", None)
        self.target = params.get("target", None)

    def split_data(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def package_results(self):
        pass

    def forecast(self):
        self.split_data()
        self.fit()
        self.predict()
        self.evaluate()
        return self.package_results()


class BaseForecasterCreator(ABC):
    forecaster_classes = {}

    def __init__(self, method, data, params):
        self.method = method
        self.data = data
        self.params = params

    def create(self):
        return self.forecaster_classes[self.method](self.data, self.params)


class BaseClassifier(ABC):
    def __init__(self, data, params):
        self.data = data
        self.params = params
        self.model = None
        self.target = params.get("target", None)

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def package_results(self):
        pass

    def classify(self):
        self.preprocess()
        self.process()
        return self.package_results()
