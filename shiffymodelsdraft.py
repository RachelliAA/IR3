import pandas as pd
import re
import nltk
from collections import Counter

from shiffy_models import model_5, model_6, model_7

nltk.download('vader_lexicon')

israel_words = [
    "Cabinet", "Colonizers", "Government", "Homeland", "Humanitarian Aid",
    "IDF", "Iron Dome", "Israel", "Israeli", "Jerusalem", "Jewish",
    "Knesset", "Mossad", "Netanyahu", "Occupation", "Occupied Territories",
    "Occupiers", "Parliament", "Settlers", "Tel Aviv", "Tel-Aviv",
    "West Bank", "West-Bank", "Zionism", "Zionist entity", "Zionist regime",
    "Zionist State", "cabinet", "colonizers", "government", "homeland",
    "humanitarian", "aid", "idf", "iron dome", "israel", "israeli",
    "jerusalem", "jewish", "knesset", "mossad", "netanyahu", "occupation",
    "occupied", "territories", "occupiers", "parliament", "settlers",
    "tel aviv", "tel-aviv", "west bank", "west-bank", "zionism",
    "zionist entity", "zionist", "regime", "zionist state"
]
palestine_words = [
    "Abbas", "Displaced", "Freedom fighters", "Gaza", "Gazans", "Hamas",
    "Hassan Nasrallah", "Hezbollah", "Houthis", "Humanitarian Crisis", "Intifada",
    "Iran", "Muhammad Sinuar", "Naim Qassem", "Nakba", "Nukhba", "Oppressed",
    "Organization", "Palestine", "Palestinians", "PLO", "Refugees", "Resistance",
    "Resisters", "Sinuar", "Terrorists", "Tyrants", "Victims", "abbas", "displaced",
    "freedom", "fighters", "gaza", "gazans", "hamas", "hassan", "nasrallah",
    "hezbollah", "houthis", "humanitarian", "crisis", "intifada", "iran",
    "muhammad", "sinuar", "naim qassem", "nakba", "nukhba", "oppressed",
    "organization", "palestine", "palestinians", "plo", "refugees", "resistance",
    "resisters", "sinuar", "terrorists", "tyrants", "victims"
]


# Function to split text into sentences
def split_into_sentences(text):
    if pd.isna(text):
        return []
    # Improved regex for better sentence splitting
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)(?=\s|$)', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]  # Remove empty sentences


# returns "I"/"P"/"N" if the sentence is purely pro israel or pro palestine or none
def check_sentence(sentence):
    israel = False
    palestine = False
    sentence = sentence.lower()
    for word in israel_words:
        if word.lower() in sentence:
            israel = True
    for word in palestine_words:
        if word.lower() in sentence:
            palestine = True
    if (palestine and israel) or (not palestine and not israel):
        return "N"
    if israel:
        return "I"
    return "P"


def check_majority(sentence):
    results = []
    for i in range(7):  # Loop from 1 to 7
        function_name = f"model_{i + 1}"  # Construct the function name as a string
        results.append(globals()[function_name](sentence))  # Call the function dynamically using globals()

    label_counts = Counter([item['label'] for item in results])
    majority_label, majority_count = label_counts.most_common(1)[0]
    majority_items = [item['score'] for item in results if item['label'] == majority_label]
    average_score = sum(majority_items) / len(majority_items) if majority_items else 0
    results.append({'label': majority_label, 'score': average_score})
    return results


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
        ip = check_sentence(title.strip())
        if ip != "N":
            models_results = check_majority(title)
            new_rows.append({
                "Newspaper": newspaper,
                "Document Number": document_number,
                "Sentence Number": sentence_number,
                "Sentence": title,
                "I/P": ip,
                "model 5 score": models_results[4]['score'],
                "model 6 score": models_results[5]['score'],
                "model 7 score": models_results[6]['score'],
                "model 5 label": models_results[4]['label'],
                "model 6 label": models_results[5]['label'],
                "model 7 label": models_results[6]['label'],
                "majority": models_results[7]['label'],
                "majority avg score": models_results[7]['score']

            })
            sentence_number = 2

        # Add body sentences starting from sentence 2
        for sentence in body_sentences:
            ip = check_sentence(sentence.strip())
            if ip != "N":
                models_results = check_majority(sentence.strip())
                new_rows.append({
                    "Newspaper": newspaper,
                    "Document Number": document_number,
                    "Sentence Number": sentence_number,
                    "Sentence": sentence.strip(),
                    "I/P": ip,
                    "model 5 score": models_results[4]['score'],
                    "model 6 score": models_results[5]['score'],
                    "model 7 score": models_results[6]['score'],
                    "model 5 label": models_results[4]['label'],
                    "model 6 label": models_results[5]['label'],
                    "model 7 label": models_results[6]['label'],
                    "majority": models_results[7]['label'],
                    "majority avg score": models_results[7]['score']
                })
                sentence_number += 1

    # Create a new DataFrame for the processed sheet
    processed_sheets[sheet_name] = pd.DataFrame(new_rows)

# Write the processed data to a new Excel file
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, processed_df in processed_sheets.items():
        processed_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Processed Excel file saved to {output_file}")
