import pandas as pd
from transformers import pipeline


def model1(sentence):
    sentiment_analysis = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    results = sentiment_analysis(sentence)
    # Accessing the first item in the list and separating the values
    sentiment = results[0]['label']
    score = results[0]['score']
    return score, sentiment


def change_word_format(sentence):
    if sentence == "neutral":
        sentence = "NEU"
    elif sentence == "positive":
        sentence = "POS"
    elif sentence == "negative":
        sentence = "NEG"
    return sentence


def main1():
    # Load the Excel file
    file_path = 'with_score.xlsx'  # Replace with your file path
    xls = pd.ExcelFile(file_path)

    # Iterate through each sheet
    for sheet_name in xls.sheet_names:
        # Load the sheet into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Check if 'Sentence' column exists
        if 'Sentence' in df.columns:
            print(f"Sheet: {sheet_name}")

            # Iterate over each sentence and get sentiment and score
            sentiments = []
            scores = []
            for sentence in df['Sentence']:
                print(sentence)
                score, sentiment = model1(sentence)
                print(score, sentiment)
                change_word_format(sentiment)  # changes the word to POS, NEG, NEU
                sentiments.append(sentiment)
                scores.append(score)

            # Add new columns with the sentiment and score
            df['model1 sentiment'] = sentiments
            df['model1 score'] = scores

            # Save the updated DataFrame back to the Excel file
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        else:
            print(f"Column 'Sentence' not found in sheet: {sheet_name}")


if __name__ == '__main__':
    main1()
