def model_1(sentence):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(sentence)
    if sentiment_score['compound'] > 0:
        return "Positive"
    elif sentiment_score['compound'] < 0:
        return "Negative"
    else:
        return "Neutral"


def model_2(sentence):
    blob = TextBlob(sentence)
    sentiment = blob.sentiment.polarity

    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"
