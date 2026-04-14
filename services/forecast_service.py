from prophet import Prophet

class BaseForecast:

    def __init__(self, df):
        self.df = df
        self.model = Prophet()

    def train(self):
        self.model.fit(self.df)

    def predict(self, periods):
        future = self.model.make_future_dataframe(periods=periods, freq="30S")
        return self.model.predict(future)