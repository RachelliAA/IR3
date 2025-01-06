import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the sentiment analysis model
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
print("uploaded model")
# Function to calculate sentiment
def get_sentiment(sentence):
    tokens = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**tokens)
    scores = torch.softmax(outputs.logits, dim=1).detach().cpu().numpy()[0]
    print(tokens,scores)
    # Map scores to sentiments
    max_score_idx = scores.argmax()
    if max_score_idx == 0 or max_score_idx == 1:
        sentiment = "NEG"
    elif max_score_idx == 2:
        sentiment = "NEU"
    else:
        sentiment = "POS"

    return scores[max_score_idx], sentiment

# Load Excel file with multiple sheets
file_path = "sentences.xlsx"  # Update with your Excel file path
excel_data = pd.ExcelFile(file_path)

updated_sheets = {}
for sheet_name in excel_data.sheet_names:
    df = excel_data.parse(sheet_name)
    if "Sentence" in df.columns:
        # Apply sentiment analysis to the 'Sentence' column
        df[["model2 score", "model2 sentiment"]] = df["Sentence"].apply(
            lambda x: pd.Series(get_sentiment(str(x)))
        )
    updated_sheets[sheet_name] = df

# Save updated Excel with new columns
output_path = "updated_file.xlsx"
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for sheet_name, df in updated_sheets.items():
        df.to_excel(writer, index=False, sheet_name=sheet_name)

print(f"Updated file saved as {output_path}")
