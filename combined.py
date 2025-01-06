# import pandas as pd
# from transformers import pipeline
#
# # Function to get sentiment and score from model
# def get_sentiment(model, sentence):
#     result = model(sentence)
#     sentiment = result[0]['label']
#     score = result[0]['score']
#     return sentiment, score
#
# # Function to process each row from the file
# def process_row(models, sentence):
#     results = {}
#     sentiments = []
#     scores = []
#
#     for i, model in enumerate(models, 1):
#         sentiment, score = get_sentiment(model, sentence)
#         sentiments.append(sentiment)
#         scores.append(score)
#         results[f'model{i} Sentiment'] = sentiment
#         results[f'model{i} score'] = score
#
#     results['sentence'] = sentence
#     return results
#
# # Main function to handle the file processing
# def main():
#     # Load the input file
#     input_file = 'sentences.xlsx'  # replace with your input file path
#     df = pd.read_excel(input_file, sheet_name=None)  # Reading all sheets
#
#     # Define models
#     models = [        pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest"),
#         pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment"),
#         pipeline("text-classification", model="cardiffnlp/twitter-xlm-roberta-base-sentiment"),
#         pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
#     ]
#
#     # Process each sheet and each row
#     for sheet_name, sheet_data in df.items():
#         # Assuming the sentences are in the first column (index 0)
#         new_data = []
#
#         for _, row in sheet_data.iterrows():
#             sentence = row[3]  # Modify if your sentence is in a different column
#             results = process_row(models, sentence)
#             new_data.append(results)
#
#         # Convert new_data to DataFrame and concatenate with the original data
#         result_df = pd.DataFrame(new_data)
#         sheet_data = pd.concat([sheet_data, result_df], axis=1)
#
#         # Save the new sheet to the output file
#         with pd.ExcelWriter('output_file.xlsx', engine='openpyxl') as writer:
#             sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
#
#     print("Processing complete. Results saved to 'output_file.xlsx'.")
#
# if __name__ == '__main__':
#     main()

# import pandas as pd
# from transformers import pipeline
#
#
# # Function to get sentiment and score from model
# def get_sentiment(model, sentence):
#     result = model(sentence)
#     sentiment = result[0]['label']
#     score = result[0]['score']
#     return sentiment, score
#
#
# # Function to process each row from the file
# def process_row(models, sentence):
#     results = {}
#     sentiments = []
#     scores = []
#
#     for i, model in enumerate(models, 1):
#         sentiment, score = get_sentiment(model, sentence)
#         sentiments.append(sentiment)
#         scores.append(score)
#         results[f'model{i} Sentiment'] = sentiment
#         results[f'model{i} score'] = score
#
#     results['sentence'] = sentence
#     return results
#
#
# # Main function to handle the file processing
# def main():
#     # Load the input file
#     input_file = 'sentences.xlsx'  # Replace with your input file path
#     output_file = 'firstFour.xlsx'  # Output file path
#
#     df = pd.read_excel(input_file, sheet_name=None)  # Reading all sheets
#
#     # Define models
#     models = [
#         pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest"),
#         pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment"),
#         pipeline("text-classification", model="cardiffnlp/twitter-xlm-roberta-base-sentiment"),
#         pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
#     ]
#
#     # Create a writer for the output Excel file
#     with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
#         # Process each sheet
#         for sheet_name, sheet_data in df.items():
#             print(f"Processing sheet: {sheet_name}")
#
#             # Assuming the sentences are in the fourth column (index 3)
#             new_data = []
#             for _, row in sheet_data.iterrows():
#                 sentence = row[3]  # Modify if your sentence is in a different column
#                 results = process_row(models, sentence)
#                 new_data.append(results)
#
#             # Convert new_data to DataFrame and concatenate with the original data
#             result_df = pd.DataFrame(new_data)
#             updated_sheet_data = pd.concat([sheet_data, result_df], axis=1)
#
#             # Save the processed sheet to the output file
#             updated_sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
#
#     print(f"Processing complete. Results saved to '{output_file}'.")
#
#
# if __name__ == '__main__':
#     main()

import pandas as pd


def standardize_sentiment(input_file, output_file=None):
    """
    Reads an Excel file, updates all 'model1 sentiment' columns with standardized values,
    and saves the updated Excel file.
    """
    # Load the Excel file
    excel_data = pd.ExcelFile(input_file)
    updated_sheets = {}

    # Define mapping for sentiment values
    sentiment_mapping = {
        "negative": "NEG",
        "positive": "POS",
        "neutral": "NEU",
    }

    # Process each sheet
    for sheet_name in excel_data.sheet_names:
        df = excel_data.parse(sheet_name)

        # Check if the sheet contains the 'model1 sentiment' column
        if "model1 sentiment" in df.columns:
            # Apply mapping to standardize sentiment values
            df["model1 sentiment"] = df["model1 sentiment"].map(sentiment_mapping).fillna(df["model1 sentiment"])

        # Store the updated DataFrame
        updated_sheets[sheet_name] = df

    # Set output file name if not provided
    if not output_file:
        output_file = input_file

    # Save the updated Excel file
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for sheet_name, df in updated_sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)

    print(f"Updated file saved as {output_file}")


# Usage
input_file_path = "with_score.xlsx"  # Update with your file path
standardize_sentiment(input_file_path)

