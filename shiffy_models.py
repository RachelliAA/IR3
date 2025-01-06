# # 5
# from transformers import pipeline
#
# distilled_student_sentiment_classifier = pipeline(
#     model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
#     return_all_scores=True
# )
#
#
# def model_5(sentence):
#     # Truncate the sentence if it exceeds the model's maximum token length
#     max_length = 512  # DistilBERT's maximum token length
#     tokens = distilled_student_sentiment_classifier.tokenizer.encode(
#         sentence, add_special_tokens=True
#     )
#     if len(tokens) > max_length:
#         truncated_sentence = distilled_student_sentiment_classifier.tokenizer.decode(
#             tokens[:max_length - 1] + [tokens[-1]],  # Include the [SEP] token
#             skip_special_tokens=True
#         )
#         sentence = truncated_sentence
#
#     # Get the classification response
#     response = distilled_student_sentiment_classifier(sentence)[0]
#     if response[0]['score'] > response[1]['score'] and response[0]['score'] > response[2]['score']:
#         return response[0]
#     if response[1]['score'] > response[2]['score']:
#         return response[1]
#     return response[2]
#
#
# # print(model_5("I love this movie and i would watch it again and again!"))
# # {'label': 'positive', 'score': 0.9731044769287109}

# 6
import requests
#
# API_URL = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"
# headers = {"Authorization": "Bearer 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"}

#
# def model_6(sentence):
#     response = (requests.post(API_URL, headers=headers, json={"inputs": sentence}).json())[0]
#     if response[0]['score'] > response[1]['score'] and response[0]['score'] > response[2]['score']:
#         return response[0]
#     if response[1]['score'] > response[2]['score']:
#         return response[1]
#     return response[2]
from transformers import pipeline

# Initialize the pipeline (assuming it's a text classification task)
model = pipeline('text-classification', model='roberta-base', tokenizer='roberta-base')

# Function to get the result in the desired format
def model_6(sentence):
    try:
        # Tokenize and classify the input sentence
        result = model(sentence)

        # Format the result as required {'label': 'negative', 'score': 0.9978852868080139}
        formatted_result = {
            'label': result[0]['label'],  # Extract the label (e.g., 'negative', 'positive')
            'score': result[0]['score']   # Extract the score (probability)
        }
        return formatted_result
    except Exception as e:
        raise RuntimeError(f"An error occurred during model inference: {e}")

# Test the function with an example sentence
sentence = "I love this product!"  # Example input sentence
result = model_6(sentence)
print(result)



# to do!!! change NEG to negative, etc

# print(model_6("don't you dare do that ever again!"))
# {'label': 'NEG', 'score': 0.9705923199653625}

# 7
# classifier = pipeline("text-classification", model="j-hartmann/sentiment-roberta-large-english-3-classes",
#                       return_all_scores=True)
#
#
# def model_7(sentence):
#     response = (classifier(sentence))[0]
#     if response[0]['score'] > response[1]['score'] and response[0]['score'] > response[2]['score']:
#         return response[0]
#     if response[1]['score'] > response[2]['score']:
#         return response[1]
#     return response[2]
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

# Load model and tokenizer locally
# model_name = "j-hartmann/sentiment-roberta-large-english-3-classes"
# tokenizer = RobertaTokenizer.from_pretrained(model_name)
# model = RobertaForSequenceClassification.from_pretrained(model_name)
#
# def model_7(sentence):
#     # Tokenize input
#     inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
#
#     # Get model predictions
#     with torch.no_grad():
#         outputs = model(**inputs)
#
#     # Extract scores from outputs
#     logits = outputs.logits
#     scores = torch.nn.functional.softmax(logits, dim=-1).squeeze().tolist()
#
#     # Find the class with the highest score
#     max_score_idx = scores.index(max(scores))
#
#     # Define the labels corresponding to the model's output classes (modify as needed)
#     labels = ['negative', 'neutral', 'positive']
#
#     return {"label": labels[max_score_idx], "score": scores[max_score_idx]}
#
# # Example usage
# sentence = "I love this product!"
# result = model_7(sentence)
# print(result)

# print(model_7("the plate was a little small and lonely looking"))
# {'label': 'negative', 'score': 0.9978852868080139}
