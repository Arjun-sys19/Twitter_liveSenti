import time
import tweepy
from transformers import pipeline
from dotenv import load_dotenv
import os


load_dotenv("api.env")


BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)


sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_sentiment(text):
    """Analyze sentiment of the given text."""
    return sentiment_pipeline(text)

def fetch_tweets(keyword, max_results=3):
    """Fetch recent tweets and handle rate limits."""
    try:
        response = client.search_recent_tweets(
            query=keyword,
            max_results=max_results, 
            tweet_fields=["created_at", "lang"],
            expansions=["author_id"]
        )
        return response.data if response.data else []
    
    except tweepy.TooManyRequests:
        print("⚠️ Rate limit exceeded. Waiting 60 seconds before retrying...")
        time.sleep(60)  
        return fetch_tweets(keyword, max_results)

if __name__ == "__main__":
    keyword = "NEAR Protocol"
    tweets = fetch_tweets(keyword, max_results=3)

    for tweet in tweets:
        sentiment = analyze_sentiment(tweet.text)
        print(f"Tweet: {tweet.text}\nSentiment: {sentiment}\n")

    print("✅ Finished processing tweets!")
