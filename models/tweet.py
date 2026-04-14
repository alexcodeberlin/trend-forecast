from elasticsearch_dsl import Document, Date, Float, Integer, Keyword, Text

class Tweet(Document):
    tweet_id = Keyword()
    timestamp = Date()
    sentiment_score = Float()
    likes = Integer()
    retweets = Integer()
    replies = Integer()
    clicks = Integer()
    text = Text()
    user_location = Text()
    followers = Integer()
    regular_engagement = Integer()
    google_engagement = Float()
    high_follower_engagement = Float()
    adjusted_engagement = Float()
    engagement_including_sentiment = Float()
    engagement_final = Float()

    class Index:
        name = "twitter_datav7"