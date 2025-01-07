import os
import pandas as pd

# Load the Excel file
file_path = "with_avg_and_maj.xlsx"  # Replace with your file path
excel_data = pd.ExcelFile(file_path)  # Load all sheets

# Define the output file
output_file = "final_file.xlsx"

# Check if the output file exists
file_exists = os.path.exists(output_file)

# Iterate through each sheet
for sheet_name in excel_data.sheet_names:
    print(f"Processing sheet: {sheet_name}")
    df = excel_data.parse(sheet_name)  # Parse the current sheet

    # Check if the required columns exist
    if "I/P" not in df.columns or "majority sentiment" not in df.columns:
        print(f"Sheet '{sheet_name}' is missing 'I/P' or 'majority sentiment' columns. Skipping.")
        continue

    # Add the 'final' column with the specified logic
    def comparison_logic(row):
        ip_value = row["I/P"]
        maj_value = row["majority sentiment"]

        if maj_value == "NEU":
            return ""  # Leave blank if sentiment is neutral

        if ip_value == "P" and maj_value == "POS":
            return "P"
        elif ip_value == "I" and maj_value == "NEG":
            return "P"
        elif ip_value == "P" and maj_value == "NEG":
            return "I"
        elif ip_value == "I" and maj_value == "POS":
            return "I"
        else:
            return ""  # Default to blank for any other case

    df["final"] = df.apply(comparison_logic, axis=1)

    # Count the occurrences of "I" and "P" in the 'final' column
    count_I = df["final"].value_counts().get("I", 0)  # Default to 0 if "I" is not found
    count_P = df["final"].value_counts().get("P", 0)  # Default to 0 if "P" is not found

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        "Summary": ["Count of I", "Count of P"],
        "Value": [count_I, count_P]
    })

    # Add the summary to the bottom of the sheet
    df_with_summary = pd.concat([df, pd.DataFrame([[""] * len(df.columns)], columns=df.columns), summary_df], ignore_index=True)

    # Save the updated sheet to the new Excel file
    with pd.ExcelWriter(output_file, mode='a' if file_exists else 'w', engine='openpyxl') as writer:
        df_with_summary.to_excel(writer, sheet_name=sheet_name, index=False)
        file_exists = True  # Update the flag once the file is created

print(f"Processing completed. Updated Excel file saved to '{output_file}'.")
