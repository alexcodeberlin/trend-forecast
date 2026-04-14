import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

from services.twitter_service import TwitterService
from services.sqlite_service import SQLiteService
from services.forecast_service import BaseForecast

twitter = TwitterService()
db = SQLiteService()

# -------------------------
# FIX: Prophet requires NO timezone
# -------------------------
def clean_df(df: pd.DataFrame):
    if df is None or df.empty:
        return df
    df["ds"] = pd.to_datetime(df["ds"], utc=True).dt.tz_convert(None)
    return df


def render():

    st.title("📊 Future Trend & Sentiment Prediction")

    dataset_choice = st.sidebar.radio(
        "Select Dataset:",
        [
            "Google Trends",
            "Twitter Sentiment",
            "Engagement Overview",
            "Favourite Overview",
            "Register and Login",
            "Shared plots"
        ]
    )

    if dataset_choice in ["Google Trends", "Twitter Sentiment", "Engagement Overview"]:
        forecast_seconds = st.sidebar.slider(
            "Select number of seconds to predict:",
            30, 3600, 1800, 30
        )

    # -------------------------
    # GOOGLE TRENDS
    # -------------------------
    if dataset_choice == "Google Trends":
        st.warning("Google Trends not implemented yet")

    # -------------------------
    # TWITTER SENTIMENT
    # -------------------------
    elif dataset_choice == "Twitter Sentiment":

        df = pd.DataFrame(twitter.load_sentiment())
        df = clean_df(df)

        st.subheader("💬 Predicting Twitter Sentiment")

        if df.empty:
            st.warning("No data available")
            return

        model = BaseForecast(df)
        model.train()
        forecast = model.predict(forecast_seconds)

        st.line_chart(df.set_index("ds")["y"])
        st.line_chart(forecast.set_index("ds")["yhat"])

        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(20))

    # -------------------------
    # ENGAGEMENT OVERVIEW
    # -------------------------
    elif dataset_choice == "Engagement Overview":

        df = pd.DataFrame(twitter.load_engagement_final())
        df = clean_df(df)

        st.subheader("📣 Engagement Metrics")

        if df.empty:
            st.warning("No data available")
            return

        st.line_chart(df.set_index("ds")["y"])

        model = BaseForecast(df)
        model.train()
        forecast = model.predict(forecast_seconds)

        st.line_chart(forecast.set_index("ds")["yhat"])

        if st.button("🔍 Save Engagement Final Data to Database"):
            db.save(df["ds"].astype(str), df["y"])
            st.success("Saved!")

        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(20))

        # -------------------------
        # METRICS LOOP (FIXED)
        # -------------------------
        metrics = [
            "regular_engagement",
            "google_engagement",
            "adjusted_engagement",
            "engagement_including_sentiment",
            "high_follower_engagement"
        ]

        for metric in metrics:

            df_m = pd.DataFrame(twitter.load_metric(metric))
            df_m = clean_df(df_m)

            if df_m.empty:
                st.warning(f"No data for {metric}")
                continue

            st.subheader(metric.replace("_", " ").title())
            st.line_chart(df_m.set_index("ds")["y"])

            model = BaseForecast(df_m)
            model.train()
            forecast_m = model.predict(forecast_seconds)

            st.line_chart(forecast_m.set_index("ds")["yhat"])

    # -------------------------
    # FAVOURITES
    # -------------------------
    elif dataset_choice == "Favourite Overview":

        data = db.get_all()
        df = pd.DataFrame(data, columns=["id", "x", "y"])

        st.subheader("🔖 Saved Data")

        if df.empty:
            st.warning("No data")
        else:
            df["x"] = pd.to_datetime(df["x"], errors="coerce")

            st.dataframe(df)

            fig, ax = plt.subplots()
            ax.plot(df["x"], df["y"])
            st.pyplot(fig)

    # -------------------------
    # LOGIN
    # -------------------------
    elif dataset_choice == "Register and Login":

        st.subheader("🔐 Auth System")
        st.info("Login not implemented yet")

    # -------------------------
    # SHARED PLOTS
    # -------------------------
    elif dataset_choice == "Shared plots":

        st.subheader("📊 Shared Analytics")

        df = pd.DataFrame(twitter.load_sentiment())
        df = clean_df(df)

        if not df.empty:
            st.line_chart(df.set_index("ds")["y"])