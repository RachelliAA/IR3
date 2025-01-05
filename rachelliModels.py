from transformers import pipeline
#1
def main1():
    from transformers import pipeline
    sentiment_analysis = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    print(sentiment_analysis("I love this!"))




def main2():
    from transformers import pipeline
    sentiment_analysis = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    print(sentiment_analysis("I hate you!"))


#3

def main3():
    # Use a pipeline as a high-level helper
    pipe = pipeline("text-classification", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

    # Example sentence for sentiment classification
    sentence = "It's an okay experience, not great, but not bad either."

    # Perform sentiment analysis
    result = pipe(sentence)

    # Print the result
    print(result)


#4
def main4():
    from transformers import pipeline
    sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
    print(sentiment_analysis("I love this!"))


if __name__ == '__main__':

    main1()
    # main2()
    # main3()
    # main4()
