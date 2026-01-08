from textblob import TextBlob

def analyze_sentiment(text: str) -> float:
    """
    Returns sentiment polarity score between -1 and 1
    """
    if not text or not isinstance(text, str):
        return 0.0

    polarity = TextBlob(text).sentiment.polarity
    return round(polarity, 2)


def sentiment_label(score: float) -> str:
    """
    Converts sentiment score into human-readable label
    """
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    return "Neutral"
