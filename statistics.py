import pandas as pd

# Load the Excel file (change 'your_file.xlsx' to your actual file name)
file_path = 'with_avg_and_maj.xlsx'
excel_data = pd.ExcelFile(file_path)

# Dictionary to store statistics for each sheet
statistics = {}

# Iterate through each sheet in the Excel file
for sheet_name in excel_data.sheet_names:
    # Read the sheet into a DataFrame
    df = excel_data.parse(sheet_name)

    # Ensure the required columns are present
    if 'I/P' in df.columns and 'majority sentiment' in df.columns:
        # Group by the two columns and count occurrences
        counts = df.groupby(['I/P', 'majority sentiment']).size().reset_index(name='count')

        # Store the statistics for the current sheet
        statistics[sheet_name] = counts
    else:
        print(f"Sheet '{sheet_name}' is missing the required columns.")

# Display the results
for sheet, stats in statistics.items():
    print(f"\nStatistics for sheet: {sheet}")
    print(stats)

# # Optionally, save the results to a new Excel file
# output_path = 'output_statistics.xlsx'
# with pd.ExcelWriter(output_path) as writer:
#     for sheet, stats in statistics.items():
#         stats.to_excel(writer, sheet_name=sheet, index=False)
#
# print(f"\nStatistics have been saved to {output_path}.")
