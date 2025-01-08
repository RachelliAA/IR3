

import pandas as pd
import matplotlib.pyplot as plt

# Load the final Excel file
file_path = "final_file.xlsx"
excel_data = pd.ExcelFile(file_path)

# Iterate through each sheet and create pie charts
for sheet_name in excel_data.sheet_names:
    # Read the sheet
    df = excel_data.parse(sheet_name)

    # Ensure the 'final' column exists
    if "final" not in df.columns:
        print(f"Sheet '{sheet_name}' is missing the 'final' column. Skipping.")
        continue

    # Calculate counts for P, I, and blank (neutral)
    count_P = df["final"].value_counts().get("P", 0)
    count_I = df["final"].value_counts().get("I", 0)
    count_blank = len(df) - (count_P + count_I)  # Total rows minus rows with "P" or "I"

    # Calculate percentages
    total = count_P + count_I + count_blank
    percentages = {
        "P": (count_P / total) * 100,
        "I": (count_I / total) * 100,
        "Neutral (Blank)": (count_blank / total) * 100,
    }

    # Plot the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(
        percentages.values(),
        labels=percentages.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=["#4CAF50", "#FF5722", "#9E9E9E"],  # Colors for P, I, and neutral
    )
    plt.title(f"Distribution in Sheet: {sheet_name}")
    plt.show()
