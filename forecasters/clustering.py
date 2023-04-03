# Third-Party Libraries
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.cluster import SpectralClustering as Spectral
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from .base import BaseForecaster, BaseForecasterCreator


class BaseClustering(BaseForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def split_data(self):
        self.train = self.data[self.features]
        self.test = self.data[self.target]

    def fit(self):
        self.model.fit(self.train)

    def predict(self):
        self.train_pred = self.model.predict(self.train)
        self.test_pred = self.model.predict(self.test)

    def evaluate(self):
        self.silhouette_score = silhouette_score(self.train, self.train_pred)

    def package_results(self):
        lables = self.model.labels_
        centroids = self.model.cluster_centers_
        # todo: change this to return a dictionary
        return {
            "model": self.model,
            "lables": lables,
            "centroids": centroids,
            "test_pred": self.test_pred,
        }


class KMeansClustering(BaseClustering):
    def __init__(self, data, params):
        super().__init__(data, params)
        n_clusters = self.params.get("n_clusters", 8)
        self.model = KMeans(n_clusters=n_clusters)


class HierarchicalClustering(BaseClustering):
    def __init__(self, data, params):
        super().__init__(data, params)
        n_clusters = self.params.get("n_clusters", 8)
        affinity = self.params.get("affinity", "euclidean")
        linkage = self.params.get("linkage", "ward")
        self.model = AgglomerativeClustering(
            n_clusters=n_clusters, affinity=affinity, linkage=linkage
        )

    def predict(self):
        self.train_pred = self.model.fit_predict(self.train)
        self.test_pred = self.model.fit_predict(self.test)


class SpectralClustering(BaseClustering):
    def __init__(self, data, params):
        super().__init__(data, params)
        self.scaler = StandardScaler()
        n_clusters = self.params.get("n_clusters", 8)
        affinity = self.params.get("affinity", "nearest_neighbors")
        assign_labels = self.params.get("assign_labels", "kmeans")
        self.model = Spectral(
            n_clusters=n_clusters,
            affinity=affinity,
            assign_labels=assign_labels,
        )

    def split_data(self):
        self.train = self.scaler.fit_transform(self.data[self.features])
        self.test = self.scaler.fit_transform(self.data[self.target])

    def predict(self):
        self.train_pred = self.model.fit_predict(self.train)
        self.test_pred = self.model.fit_predict(self.test)


class DBSCANClustering(BaseClustering):
    def __init__(self, data, params):
        super().__init__(data, params)
        eps = self.params.get("eps", 0.5)
        min_samples = self.params.get("min_samples", 5)
        metric = self.params.get("metric", "euclidean")
        self.model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)

    def predict(self):
        self.train_pred = self.model.fit_predict(self.train)
        self.test_pred = self.model.fit_predict(self.test)


class GaussianMixtureClustering(BaseClustering):
    def __init__(self, data, params):
        super().__init__(data, params)
        n_components = self.params.get("n_components", 8)
        covariance_type = self.params.get("covariance_type", "full")
        self.model = GaussianMixture(
            n_components=n_components, covariance_type=covariance_type
        )

    def predict(self):
        self.train_pred = self.model.fit_predict(self.train)
        self.test_pred = self.model.fit_predict(self.test)


class ClusteringForcasterCreator(BaseForecasterCreator):
    forecaster_classes = {
        "kmeans": KMeansClustering,
        "hierarchical": HierarchicalClustering,
        "spectral": SpectralClustering,
        "dbscan": DBSCANClustering,
        "gaussian_mixture": GaussianMixtureClustering,
    }
