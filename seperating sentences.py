import pandas as pd
import re

# Function to split text into sentences
def split_into_sentences(text):
    if pd.isna(text):
        return []
    # Improved regex for better sentence splitting
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)(?=\s|$)', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]  # Remove empty sentences

# Load the original Excel file
input_file = "posts_first_targil.xlsx"  # Replace with the path to your file
output_file = "sentences.xlsx"

# Read all sheets into a dictionary of DataFrames
sheets = pd.read_excel(input_file, sheet_name=None)

processed_sheets = {}

# Process each sheet
for sheet_name, df in sheets.items():
    new_rows = []

    # Iterate through each row in the sheet
    for idx, row in df.iterrows():
        newspaper = row.get("Newspaper", "Unknown")
        title = row.get("title", "")
        body_text = row.get("Body Text", "")

        # Split title and body text into sentences

        body_sentences = split_into_sentences(body_text)

        # Add title sentence as sentence 1
        document_number = idx + 1  # Assuming document number corresponds to row index
        sentence_number = 1

        new_rows.append({
            "Newspaper": newspaper,
            "Document Number": document_number,
            "Sentence Number": 1,
            "Sentence": title
        })
        sentence_number =2

        # Add body sentences starting from sentence 2
        for sentence in body_sentences:
            new_rows.append({
                "Newspaper": newspaper,
                "Document Number": document_number,
                "Sentence Number": sentence_number,
                "Sentence": sentence.strip(),
            })
            sentence_number += 1

    # Create a new DataFrame for the processed sheet
    processed_sheets[sheet_name] = pd.DataFrame(new_rows)

# Write the processed data to a new Excel file
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, processed_df in processed_sheets.items():
        processed_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Processed Excel file saved to {output_file}")
