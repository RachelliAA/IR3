from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

# Load the tokenizer and model
model_name = "finiteautomata/bertweet-base-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create a sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_sentence(sentence):
    """
    Analyzes the semantics (sentiment) of the given sentence.

    :param sentence: str, the input sentence to analyze
    :return: str, the sentiment result
    """
    results = sentiment_analyzer(sentence)
    sentiment = results[0]['label']
    score = results[0]['score']
    return f"Sentiment: {sentiment}, Confidence Score: {score:.2f}"

# Example usage
if __name__ == "__main__":
    sentence = input("Enter a sentence to analyze: ")
    result = analyze_sentence(sentence)
    print(result)
