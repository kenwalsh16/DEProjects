import easygui
import pandas as pd

csv_file = easygui.fileopenbox(title="Select a CSV file", filetypes=["*.csv"])

if csv_file:
    df = pd.read_csv(csv_file)
    print(df.head(6))  # Print first 6 rows of the dataframe
else:
    print("No file was selected!")