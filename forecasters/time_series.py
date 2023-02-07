import numpy as np
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout


class BaseForecaster(ABC):
    def __init__(self, data, params):
        self.data = data
        self.params = params
        self.model = None
        self.features = params.get('features', None)
        self.target = params.get('target', None)
        self.window = params.get('window', 1)

    def split_data(self):
        rate = self.params.get('rate', 0.2)
        random_state = self.params.get('random_state', 3)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.data[self.features],
            self.data[self.target],
            test_size=rate,
            random_state=random_state
        )

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


class LinearRegressionForecaster(BaseForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        self.model = LinearRegression()
        self.model.fit(self.x_train, self.y_train)

    def predict(self):
        self.y_pred = self.model.predict(self.x_test)

    def evaluate(self):
        self.score = self.model.score(self.x_test, self.y_test)

    def package_results(self):
        return {
            'model': self.model,
            'x_train': self.x_train,
            'x_test': self.x_test,
            'y_train': self.y_train,
            'y_test': self.y_test,
            'y_pred': self.y_pred,
            'score': self.score
        }


class MoveAverageForecaster(BaseForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def split_data(self):
        pass

    def fit(self):
        pass

    def predict(self):
        self.y_pred = self.data[self.target].rolling(window=self.window).mean()

    def evaluate(self):
        self.score = self.data[self.target].corr(self.y_pred)

    def package_results(self):
        return {
            'y_pred': self.y_pred,
            'score': self.score
        }


class LSTMForecaster(BaseForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)
        self.model = Sequential()
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def split_data(self):
        rate = self.params.get('rate', 0.2)
        random_state = self.params.get('random_state', 3)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.data[self.features],
            self.data[self.target],
            test_size=rate,
            random_state=random_state
        )
        scaled_data = self.scaler.fit_transform(self.data[self.features])
        self.x_train = self.scaler.fit_transform(self.x_train)
        self.x_test = self.scaler.transform(self.x_test)
        prev = self.params.get('prev', 1)
        for x in range(prev, len(scaled_data)):
            self.x_train.append(scaled_data[x - prev:x, 0])
            self.y_train.append(scaled_data[x, 0])
        self.x_train, self.y_train = (
            np.array(self.x_train), np.array(self.y_train)
        )
        self.x_train = np.reshape(
            self.x_train, (self.x_train.shape[0], self.x_train.shape[1], 1)
        )

    def fit(self):
        self.model.add(LSTM(
            units=50, return_sequences=True, input_shape=(self.x_train.shape[1], 1)
        ))
        self.model.add(Dropout(self.params.get('dropout', 0.2)))
        self.model.add(Dense(units=1))
        self.model.compile(
            optimizer=self.params.get('optimizer', 'adam'),
            loss=self.params.get('loss', 'mean_squared_error')
        )
        self.model.fit(
            self.x_train, self.y_train, epochs=self.params.get('epochs', 1),
            batch_size=self.params.get('batch_size', 32)
        )

    def predict(self):
        self.train_pred = self.model.predict(self.x_train)
        self.test_pred = self.model.predict(self.x_test)
        self.train_pred = self.scaler.inverse_transform(self.train_pred)
        self.test_pred = self.scaler.inverse_transform(self.test_pred)

    def evaluate(self):
        self.y_train = self.scaler.inverse_transform(self.y_train)
        self.y_test = self.scaler.inverse_transform(self.y_test)
        self.train_score = np.sqrt(
            mean_squared_error(self.y_train, self.train_pred)
        )
        self.test_score = np.sqrt(
            mean_squared_error(self.y_test, self.test_pred)
        )

    def package_results(self):
        return {
            'model': self.model,
            'x_train': self.x_train,
            'x_test': self.x_test,
            'y_train': self.y_train,
            'y_test': self.y_test,
            'train_pred': self.train_pred,
            'test_pred': self.test_pred,
            'train_score': self.train_score,
            'test_score': self.test_score
        }


class SimpleExponentialSmoothingForecaster(BaseForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        alpha = self.params.get('alpha', 0.2)
        optimazed = self.params.get('optimazed', False)
        initialization_method = self.params.get(
            'initialization_method', 'estimated')
        self.model = SimpleExpSmoothing(self.y_train, initialization_method=initialization_method).fit(
            optimized=optimazed, smoothing_level=alpha
        )

    def predict(self):
        predays = self.params.get('predays', 1)
        self.y_pred = self.model.forecast(predays)

    def evaluate(self):
        self.score = self.y_test.corr(self.y_pred)

    def package_results(self):
        return {
            'model': self.model,
            'x_train': self.x_train,
            'x_test': self.x_test,
            'y_train': self.y_train,
            'y_test': self.y_test,
            'y_pred': self.y_pred,
            'score': self.score
        }


class HoltForecaster(SimpleExponentialSmoothingForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        alpha = self.params.get('alpha', 0.2)
        beta = self.params.get('beta', 0.2)
        optimazed = self.params.get('optimazed', False)
        initialization_method = self.params.get(
            'initialization_method', 'estimated')
        self.model = Holt(self.y_train, initialization_method=initialization_method).fit(
            optimized=optimazed, smoothing_level=alpha, smoothing_slope=beta
        )


class HoltWintersSeasonalForecaster(SimpleExponentialSmoothingForecaster):

    def fit(self):
        # add, mul, additive, multiplicative, None
        add_trend = self.params.get('add_trend', 'add')
        add_seasonality = self.params.get('add_seasonality', 'add')
        self.model = ExponentialSmoothing(
            self.y_train,
            trend=add_trend,
            seasonal=add_seasonality,
            seasonal_periods=self.window
        ).fit()


class ArimaForcaster(BaseForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        autoregressive = self.params.get('autoregressive', 1)
        moving_average = self.params.get('moving_average', 1)
        differences = self.params.get('differences', 1)
        self.model = ARIMA(self.y_train, order=(
            autoregressive, differences, moving_average
        )).fit()

    def predict(self):
        predays = self.params.get('predays', 1)
        self.train_pred = self.model.predict(
            start=0, end=len(self.y_train) - 1)
        self.test_pred = self.model.predict(
            start=len(self.y_train), end=len(self.y_train) + predays - 1
        )

    def evaluate(self):
        self.train_score = np.sqrt(
            mean_squared_error(self.y_train, self.train_pred)
        )
        self.test_score = np.sqrt(
            mean_squared_error(self.y_test, self.test_pred)
        )

    def package_results(self):
        return {
            'model': self.model,
            'x_train': self.x_train,
            'x_test': self.x_test,
            'y_train': self.y_train,
            'y_test': self.y_test,
            'train_pred': self.train_pred,
            'test_pred': self.test_pred,
            'train_score': self.train_score,
            'test_score': self.test_score
        }


class SarimaForcaster(ArimaForcaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        autoregressive = self.params.get('autoregressive', 1)
        moving_average = self.params.get('moving_average', 1)
        differences = self.params.get('differences', 1)
        seasonal_autoregressive = self.params.get('seasonal_autoregressive', 1)
        seasonal_moving_average = self.params.get('seasonal_moving_average', 1)
        seasonal_differences = self.params.get('seasonal_differences', 1)
        self.model = SARIMAX(
            self.y_train,
            order=(autoregressive, differences, moving_average),
            seasonal_order=(
                seasonal_autoregressive, seasonal_differences, seasonal_moving_average, self.window
            )
        ).fit()


class ModelCreator:
    ModelMap = {}

    def __init__(self, type):
        self.type = type

    def create_model(self, data, params):
        return self.ModelMap[self.type](self.type, data, params)

    @staticmethod
    def register_model(model_type):
        def decorator(model):
            ModelCreator.ModelMap[model_type] = model
            return model

        return decorator
