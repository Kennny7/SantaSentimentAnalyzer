from typing import NamedTuple
from textblob import TextBlob

class SentimentResult(NamedTuple):
    """
    Represents the result of sentiment analysis.
    Attributes:
        sentiment (str): The classified sentiment ('Positive', 'Negative', 'Neutral').
        score (float): The sentiment polarity score.
    """
    sentiment: str
    score: float

def analyze_sentiment(message: str) -> SentimentResult:
    """
    Analyze the sentiment of a given message using TextBlob.
    Args:
        message (str): The input message to analyze.
    Returns:
        SentimentResult: The sentiment classification and polarity score.
    Raises:
        ValueError: If the input message is empty or None.
    """
    if not message or not isinstance(message, str):
        raise ValueError("Message must be a non-empty string.")

    # Analyze the sentiment
    blob = TextBlob(message)
    polarity = blob.sentiment.polarity

    # Classify the sentiment
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return SentimentResult(sentiment=sentiment, score=polarity)
