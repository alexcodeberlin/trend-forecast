import streamlit as st

class PlotService:

    @staticmethod
    def plot_past(df, title, ylabel):
        st.subheader(title)
        st.line_chart(df.set_index("ds")["y"])

    @staticmethod
    def plot_forecast(df, forecast, title):
        st.subheader(title)
        st.line_chart(forecast.set_index("ds")["yhat"])