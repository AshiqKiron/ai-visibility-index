from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(text: str) -> dict:
    """
    Returns a dict with neg, neu, pos, and compound scores.
    Compound score: -1 (most negative) to +1 (most positive).
    """
    return analyzer.polarity_scores(text)

def get_sentiment_label(text: str) -> str:
    score = get_sentiment_score(text)['compound']
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"