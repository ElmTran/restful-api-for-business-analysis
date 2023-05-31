# Third-Party Libraries
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier as DecisionTree

from .base import BaseForecaster, BaseForecasterCreator


class BaseClassifier(BaseForecaster):
    def __init__(self, data, params):
        self.excludes = params.get("excludes", [])
        self.excludes.append(params.get("target", None))
        self.max_features = params.get("max_features", None)
        if self.max_features:
            data = data.sample(self.max_features)
        super().__init__(data, params)

    def split_data(self):
        rate = self.params.get("rate", 0.2)
        random_state = self.params.get("random_state", 42)
        self.dummies = self.params.get("dummies", None)
        if self.dummies:
            self.data = pd.get_dummies(
                self.data, columns=self.dummies, drop_first=True
            )
        (
            self.x_train,
            self.x_test,
            self.y_train,
            self.y_test,
        ) = train_test_split(
            self.data.drop(self.excludes, axis=1),
            self.data[self.target],
            test_size=rate,
            random_state=random_state,
        )

    def fit(self):
        self.model.fit(self.x_train, self.y_train)

    def predict(self):
        self.train_pred = self.model.predict(self.x_train)
        self.y_pred = self.model.predict(self.x_test)

    def evaluate(self):
        self.train_accuracy = (
            accuracy_score(self.y_train, self.train_pred) * 100
        )
        self.test_accuracy = accuracy_score(self.y_test, self.y_pred) * 100

    def package_results(self):
        return {
            "model": self.model,
            "x_train": self.x_train,
            "x_test": self.x_test,
            "y_train": self.y_train,
            "y_test": self.y_test,
            "train_pred": self.train_pred,
            "y_pred": self.y_pred,
            "train_accuracy": self.train_accuracy,
            "test_accuracy": self.test_accuracy,
        }


class DecisionTreeClassifier(BaseClassifier):
    def __init__(self, data, params):
        super().__init__(data, params)
        max_depth = self.params.get("max_depth", 3)
        min_samples_split = self.params.get("min_samples_split", 10)
        self.model = DecisionTree(
            max_depth=max_depth, min_samples_split=min_samples_split
        )


class NaiveBayesClassifier(BaseClassifier):
    def __init__(self, data, params):
        super().__init__(data, params)
        priors = self.params.get("priors", None)
        self.model = GaussianNB(priors=priors)


class RandomForestClassifier(BaseClassifier):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        n_estimators = self.params.get("n_estimators", 100)
        max_depth = self.params.get("max_depth", 2)
        min_samples_split = self.params.get("min_samples_split", 2)
        model_random_state = self.params.get("model_random_state", 0)
        self.tree = []
        for _ in range(n_estimators):
            tree = DecisionTree(
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=model_random_state,
            )
            tree.fit(self.x_train, self.y_train)
            self.tree.append(tree)

    def predict(self):
        predictions = []
        for tree in self.tree:
            predictions.append(tree.predict(self.x_test))
        self.y_pred = np.mean(predictions, axis=0)

    def evaluate(self):
        self.test_accuracy = accuracy_score(self.y_test, self.y_pred) * 100

    def package_results(self):
        return {
            "model": self.tree,
            "x_train": self.x_train,
            "x_test": self.x_test,
            "y_train": self.y_train,
            "y_test": self.y_test,
            "y_pred": self.y_pred,
            "test_accuracy": self.test_accuracy,
        }


class KNNClassifier(BaseClassifier):
    def __init__(self, data, params):
        super().__init__(data, params)
        n_neighbors = self.params.get("n_neighbors", 3)
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)


class SVMClassifier(BaseClassifier):
    def __init__(self, data, params):
        super().__init__(data, params)
        kernel = self.params.get("kernel", "linear")
        C_value = self.params.get("C_value", 1.0)
        self.model = SVC(kernel=kernel, C=C_value)


class LogisticRegressionClassifier(BaseClassifier):
    def __init__(self, data, params):
        super().__init__(data, params)
        self.model = LogisticRegression()


class ClassifierCreator(BaseForecasterCreator):
    forecaster_classes = {
        "decision_tree": DecisionTreeClassifier,
        "naive_bayes": NaiveBayesClassifier,
        "random_forest": RandomForestClassifier,
        "knn": KNNClassifier,
        "svm": SVMClassifier,
        "log_regression": LogisticRegressionClassifier,
    }
