# Third-Party Libraries
import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.api import ExponentialSmoothing, Holt, SimpleExpSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Project Imports
from forecasters.base import BaseForecaster, BaseForecasterCreator


class BaseTimeSeriesForecaster(BaseForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)
        self.window = params.get("window", 3)
        self.time_format = params.get("time_format", "%Y-%m-%d")

    def split_data(self):
        rate = self.params.get("rate", 0.2)
        random_state = self.params.get("random_state", None)
        # convert to datetime
        self.data[self.features[0]] = pd.to_datetime(
            self.data[self.features[0]], format=self.time_format
        )
        # sort by time
        self.data = self.data.sort_values(by=self.features[0])
        self.data["time"] = np.arange(len(self.data))
        # split data
        (
            self.x_train,
            self.x_test,
            self.y_train,
            self.y_test,
        ) = train_test_split(
            self.data[["time"]],
            self.data[self.target],
            test_size=rate,
            random_state=random_state,
            shuffle=False,
        )


class LinearRegressionForecaster(BaseTimeSeriesForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        self.model = LinearRegression()
        self.model.fit(self.x_train, self.y_train)

    def predict(self):
        self.y_pred = self.model.predict(self.x_test)
        self.data["pred"] = np.nan
        self.data.loc[self.x_test.index, "pred"] = self.y_pred

        # predict future
        predays = self.params["predays"]  # number of features
        last_time = self.data["time"].iloc[-1]
        future_time = np.arange(last_time + 1, last_time + predays + 1)
        future_pred = self.model.predict(future_time.reshape(-1, 1))
        # add future time to data
        self.data = self.data.append(
            pd.DataFrame(
                {
                    "time": future_time,
                    "pred": future_pred,
                }
            )
        )

    def evaluate(self):
        self.score = self.model.score(self.x_test, self.y_test)

    def package_results(self):
        return {
            "result": {
                "model": "LinearRegression",
                "score": self.score,
            },
            "file": self.generate_result_file(),
        }


class MoveAverageForecaster(BaseTimeSeriesForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def split_data(self):
        pass

    def fit(self):
        pass

    def predict(self):
        self.roll_mean = (
            self.data[self.target].rolling(window=self.window).mean()
        )
        last_roll_mean = self.roll_mean.iloc[-self.window]
        self.data["pred"] = self.roll_mean
        predays = self.params["predays"]  # number of features
        predictions = pd.DataFrame(
            {"pred": np.repeat(last_roll_mean, predays)}
        )
        self.data = self.data.append(predictions)

    def evaluate(self):
        self.score = self.data[self.target].corr(self.roll_mean)

    def package_results(self):
        return {
            "result": {
                "model": "MoveAverage",
                "score": self.score,
            },
            "file": self.generate_result_file(),
        }


class LSTMForecaster(BaseTimeSeriesForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)
        self.model = Sequential()
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def split_data(self):
        rate = self.params.get("rate", 0.2)
        random_state = self.params.get("random_state", 3)
        self.data[self.features[0]] = pd.to_datetime(
            self.data[self.features[0]], format=self.time_format
        )
        self.data = self.data.sort_values(by=self.features[0])
        self.data["time"] = np.arange(len(self.data))
        self.data[f"{self.target}_tr"] = self.scaler.fit_transform(
            self.data[[self.target]]
        )
        (
            self.x_train,
            self.x_test,
            self.y_train,
            self.y_test,
        ) = train_test_split(
            self.data[["time"]],
            self.data[f"{self.target}_tr"],
            test_size=rate,
            random_state=random_state,
            shuffle=False,
        )

    def fit(self):
        self.model.add(
            LSTM(
                units=50,
                return_sequences=True,
                input_shape=(self.x_train.shape[1], 1),
            )
        )
        self.model.add(Dropout(self.params.get("dropout", 0.2)))
        self.model.add(Dense(units=1))
        self.model.compile(
            optimizer=self.params.get("optimizer", "adam"),
            loss=self.params.get("loss", "mean_squared_error"),
        )
        self.model.fit(
            self.x_train,
            self.y_train,
            epochs=self.params.get("epochs", 1),
            batch_size=self.params.get("batch_size", 32),
        )

    def predict(self):
        self.y_pred = self.scaler.inverse_transform(
            [r[0] for r in self.model.predict(self.x_test)]
        )
        self.data["pred"] = np.nan
        self.data.loc[self.x_test.index, "pred"] = self.y_pred
        # predict future
        predays = self.params["predays"]  # number of features
        future_frame = pd.DataFrame(
            {"time": np.arange(len(self.data), len(self.data) + predays)}
        )
        future_pred = self.scaler.inverse_transform(
            [r[0] for r in self.model.predict(future_frame)]
        )
        # add future time to data
        future_frame["pred"] = future_pred
        self.data = self.data.append(future_frame)

    def evaluate(self):
        self.score = np.sqrt(mean_squared_error(self.y_test, self.y_pred))

    def package_results(self):
        return {
            "result": {
                "model": "LSTM",
                "RMSE": self.score,
            },
            "file": self.generate_result_file(),
        }


class SimpleExponentialSmoothingForecaster(BaseTimeSeriesForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        alpha = self.params.get("alpha", 0.2)
        optimazed = self.params.get("optimazed", False)
        initialization_method = self.params.get(
            "initialization_method", "estimated"
        )
        self.model = SimpleExpSmoothing(
            self.y_train, initialization_method=initialization_method
        ).fit(optimized=optimazed, smoothing_level=alpha)

    def predict(self):
        self.y_pred = self.model.forecast(len(self.y_test))
        self.data["pred"] = np.nan
        self.data.loc[self.y_test.index, "pred"] = self.y_pred
        predays = self.params.get("predays", 30)
        self.future_pred = self.model.forecast(len(self.y_test) + predays)
        self.data = self.data.append(
            pd.DataFrame({"pred": self.future_pred[-predays:]})
        )

    def evaluate(self):
        self.score = np.sqrt(mean_squared_error(self.y_test, self.y_pred))

    def package_results(self):
        return {
            "result": {
                "model": "SimpleExponentialSmoothing",
                "score": self.score,
            },
            "file": self.generate_result_file(),
        }


class HoltForecaster(SimpleExponentialSmoothingForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        alpha = self.params.get("alpha", 0.2)
        beta = self.params.get("beta", 0.2)
        optimazed = self.params.get("optimazed", False)
        initialization_method = self.params.get(
            "initialization_method", "estimated"
        )
        self.model = Holt(
            self.y_train, initialization_method=initialization_method
        ).fit(optimized=optimazed, smoothing_level=alpha, smoothing_slope=beta)


class HoltWintersSeasonalForecaster(SimpleExponentialSmoothingForecaster):
    def fit(self):
        # add, mul, additive, multiplicative, None
        add_trend = self.params.get("add_trend", "add")
        add_seasonality = self.params.get("add_seasonality", "add")
        self.model = ExponentialSmoothing(
            self.y_train,
            trend=add_trend,
            seasonal=add_seasonality,
            seasonal_periods=self.window,
        ).fit()


class ArimaForcaster(BaseTimeSeriesForecaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        autoregressive = self.params.get("autoregressive", 1)
        moving_average = self.params.get("moving_average", 1)
        differences = self.params.get("differences", 1)
        self.model = ARIMA(
            self.y_train, order=(autoregressive, differences, moving_average)
        ).fit()

    def predict(self):
        self.data["pred"] = np.nan
        self.test_pred = self.model.predict(
            start=len(self.y_train),
            end=len(self.y_train) + len(self.y_test) - 1,
        )
        self.data["pred"][-len(self.test_pred) :] = self.test_pred
        predays = self.params.get("predays", 5)
        future_pred = self.model.predict(
            start=self.data.index[-1] + 1,
            end=self.data.index[-1] + predays,
        )
        self.data = self.data.append(pd.DataFrame({"pred": future_pred}))

    def evaluate(self):
        self.score = np.sqrt(mean_squared_error(self.y_test, self.test_pred))

    def package_results(self):
        return {
            "result": {
                "model": "ARIMA",
                "RMSE": self.score,
            },
            "file": self.generate_result_file(),
        }


class SarimaForcaster(ArimaForcaster):
    def __init__(self, data, params):
        super().__init__(data, params)

    def fit(self):
        autoregressive = self.params.get("autoregressive", 1)
        moving_average = self.params.get("moving_average", 1)
        differences = self.params.get("differences", 1)
        seasonal_autoregressive = self.params.get("seasonal_autoregressive", 1)
        seasonal_moving_average = self.params.get("seasonal_moving_average", 1)
        seasonal_differences = self.params.get("seasonal_differences", 1)
        self.model = SARIMAX(
            self.y_train,
            order=(autoregressive, differences, moving_average),
            seasonal_order=(
                seasonal_autoregressive,
                seasonal_differences,
                seasonal_moving_average,
                self.window,
            ),
        ).fit()


class TimeSeriesForecasterCreator(BaseForecasterCreator):
    forecaster_classes = {
        "linear_regression": LinearRegressionForecaster,
        "move_average": MoveAverageForecaster,
        "lstm": LSTMForecaster,
        "simple_exponential_smoothing": SimpleExponentialSmoothingForecaster,
        "holt": HoltForecaster,
        "holt_winters_seasonal": HoltWintersSeasonalForecaster,
        "arima": ArimaForcaster,
    }
