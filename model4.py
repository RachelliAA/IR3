import pandas as pd
from transformers import pipeline

def main4():
    # Initialize the sentiment analysis pipeline with the new model
    pipe = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")

    # Path to your Excel file
    file_path = "sentences.xlsx"
    excel_data = pd.ExcelFile(file_path)

    updated_sheets = {}

    # Function to process a single sentence
    def get_sentiment(sentence):
        print(sentence)
        try:
            result = pipe(sentence[:512])[0]  # Truncate to 512 characters if necessary
            label = result['label'].upper()
            if label == "POSITIVE":
                sentiment = "POS"
            elif label == "NEGATIVE":
                sentiment = "NEG"
            else:
                sentiment = "NEU"
            return result['score'], sentiment
        except Exception as e:
            return None, None  # Handle errors gracefully

    for sheet_name in excel_data.sheet_names:
        print(sheet_name)
        df = excel_data.parse(sheet_name)
        if "Sentence" in df.columns:
            # Apply the pipeline to the 'Sentence' column
            df[["model4 score", "model4 sentiment"]] = df["Sentence"].apply(
                lambda x: pd.Series(get_sentiment(str(x)))
            )
        updated_sheets[sheet_name] = df

    # Save the updated Excel file
    output_path = "updated_file4.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in updated_sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)

    print(f"Updated file saved as {output_path}")

# Call the main4 function
main4()
