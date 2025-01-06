
import pandas as pd

# Read the Excel file with multiple sheets into a dictionary
sheets = pd.read_excel('with_score.xlsx', sheet_name=None)

# Function to calculate average score and majority label for each sheet
def process_sheet(df):
    # Find columns that contain the word "score" in the header (case-insensitive)
    score_columns = [col for col in df.columns if 'score' in col.lower()]

    # Calculate the average score for each row
    df['average score'] = df[score_columns].mean(axis=1)

    # Find columns that contain the word "sentiment" in the header (case-insensitive)
    sentiment_columns = [col for col in df.columns if 'sentiment' in col.lower()]

    # Function to find the majority sentiment label for each row
    def majority_label(row):
        sentiments = row[sentiment_columns]
        return sentiments.mode()[0] if not sentiments.empty else None

    # Apply the majority_label function to each row
    df['majority label'] = df.apply(majority_label, axis=1)

    return df

# Process each sheet and save the modified DataFrame back
processed_sheets = {}
for sheet_name, df in sheets.items():
    processed_sheets[sheet_name] = process_sheet(df)

# Save the processed sheets to a new Excel file
with pd.ExcelWriter('with_avg2.xlsx') as writer:
    for sheet_name, df in processed_sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Processing complete. The output is saved to 'output_file.xlsx'.")
