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
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the model and tokenizer locally
MODEL_NAME = "finiteautomata/bertweet-base-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def model_6(sentence):
    # Tokenize the input sentence
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted probabilities
    scores = torch.nn.functional.softmax(outputs.logits, dim=1)

    # Map the scores to their respective labels
    labels = ["negative", "neutral", "positive"]
    scores_dict = [{ "label": labels[i], "score": score.item()} for i, score in enumerate(scores[0])]

    # Find the best response based on the highest score
    best_response = max(scores_dict, key=lambda x: x['score'])
    return best_response

# Example usage

#print(model_6("don't you dare do that ever again!" * 20))
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
