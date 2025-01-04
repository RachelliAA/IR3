# 4
from transformers import pipeline

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    return_all_scores=True
)


def model_5(sentence):
    response = distilled_student_sentiment_classifier(sentence)[0]
    if response[0]['score'] > response[1]['score'] and response[0]['score'] > response[2]['score']:
        return response[0]
    if response[1]['score'] > response[2]['score']:
        return response[1]
    return response[2]


# print(model_5("I love this movie and i would watch it again and again!"))
# {'label': 'positive', 'score': 0.9731044769287109}

# 5
import requests

API_URL = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"
headers = {"Authorization": "Bearer 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"}


def model_6(sentence):
    response = (requests.post(API_URL, headers=headers, json={"inputs": sentence}).json())[0]
    if response[0]['score'] > response[1]['score'] and response[0]['score'] > response[2]['score']:
        return response[0]
    if response[1]['score'] > response[2]['score']:
        return response[1]
    return response[2]
#to do!!! change NEG to negative, etc

# print(model_6("don't you dare do that ever again!"))
# {'label': 'NEG', 'score': 0.9705923199653625}

classifier = pipeline("text-classification", model="j-hartmann/sentiment-roberta-large-english-3-classes",
                      return_all_scores=True)


def model_7(sentence):
    response = (classifier(sentence))[0]
    if response[0]['score'] > response[1]['score'] and response[0]['score'] > response[2]['score']:
        return response[0]
    if response[1]['score'] > response[2]['score']:
        return response[1]
    return response[2]


# print(model_7("the plate was a little small and lonely looking"))
# {'label': 'negative', 'score': 0.9978852868080139}
