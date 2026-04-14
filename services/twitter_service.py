from models.tweet import Tweet
import pandas as pd


class TwitterService:

    # -------------------------
    # FIX: helper (important for Prophet)
    # removes timezone + ensures clean format
    # -------------------------
    def _clean(self, data):
        df = pd.DataFrame(data)

        if df.empty:
            return df

        df["ds"] = pd.to_datetime(df["ds"], utc=True).dt.tz_convert(None)
        return df

    # -------------------------
    # SENTIMENT
    # -------------------------
    def load_sentiment(self):
        query = Tweet.search()[:500]
        response = query.execute()

        data = []

        for hit in response:
            if hasattr(hit, "timestamp") and hasattr(hit, "sentiment_score"):
                data.append({
                    "ds": hit.timestamp,
                    "y": hit.sentiment_score
                })

        return self._clean(data)

    # -------------------------
    # ENGAGEMENT FINAL
    # -------------------------
    def load_engagement_final(self):
        query = Tweet.search()[:500]
        response = query.execute()

        data = []

        for hit in response:
            if hasattr(hit, "timestamp") and hasattr(hit, "engagement_final"):
                data.append({
                    "ds": hit.timestamp,
                    "y": hit.engagement_final
                })

        return self._clean(data)

    # -------------------------
    # GENERIC METRIC LOADER (FIX for your crash)
    # -------------------------
    def load_metric(self, metric):
        query = Tweet.search()[:500]
        response = query.execute()

        data = []

        for hit in response:
            if hasattr(hit, "timestamp") and hasattr(hit, metric):
                data.append({
                    "ds": hit.timestamp,
                    "y": getattr(hit, metric)
                })

        return self._clean(data)