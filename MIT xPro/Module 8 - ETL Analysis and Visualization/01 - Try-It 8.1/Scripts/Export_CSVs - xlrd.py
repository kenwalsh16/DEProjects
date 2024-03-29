import os
import csv
import xlrd
import easygui

# Prompt the user to select the Excel workbook using easygui
excel_file = easygui.fileopenbox(title="Select an Excel workbook", filetypes=['*.xls', '*.xlsx'])

# Check if a file was selected
if not excel_file:
    print("No Excel file was selected. Exiting...")
    exit()

# Load the Excel workbook
workbook = xlrd.open_workbook(excel_file)

# Ensure the "CSVs" folder exists in the same directory as the Excel file
csv_folder = os.path.join(os.path.dirname(excel_file), "CSVs")
if not os.path.exists(csv_folder):
    os.mkdir(csv_folder)

# Iterate over each worksheet and export to CSV
for sheet_name in workbook.sheet_names():
    sheet = workbook.sheet_by_name(sheet_name)
    csv_filename = os.path.join(csv_folder, sheet_name + ".csv")

    with open(csv_filename, 'w', newline="", encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row_num in range(sheet.nrows):
            writer.writerow(sheet.row_values(row_num))

print(f"All worksheets from '{excel_file}' have been exported to the 'CSVs' folder.")

