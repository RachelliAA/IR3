import pandas as pd
hi
# Read the input Excel file
input_file = "posts_first_targil.xlsx"  # Replace with your actual file name
output_file = "split_sentences.xlsx"

# Load the Excel file with multiple sheets
excel_data = pd.read_excel(input_file, sheet_name=None)

# Create a dictionary to store the processed sheets
processed_sheets = {}

for sheet_name, df in excel_data.items():
    # Ensure the necessary columns exist
    if "Body Text" in df.columns and "Newspaper" in df.columns:
        processed_rows = []

        # Process each row in the DataFrame
        for document_number, row in df.iterrows():
            body_text = str(row["Body Text"])  # Convert to string to avoid errors
            newspaper = row["Newspaper"] if "Newspaper" in row else None

            # Split the body text by periods (basic sentence splitting)
            sentences = body_text.split('.')

            for sentence_number, sentence in enumerate(sentences, start=1):
                sentence = sentence.strip()  # Remove leading/trailing whitespace
                if sentence:  # Avoid empty sentences
                    processed_rows.append({
                        "Newspaper": newspaper,
                        "Document Number": document_number + 1,  # +1 to match Excel indexing
                        "Sentence Number": sentence_number,
                        "Sentence": sentence
                    })

        # Create a DataFrame for the processed rows
        processed_df = pd.DataFrame(processed_rows)
        processed_sheets[sheet_name] = processed_df

# Write the processed data to a new Excel file
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    for sheet_name, processed_df in processed_sheets.items():
        processed_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Processed Excel file saved as {output_file}")
