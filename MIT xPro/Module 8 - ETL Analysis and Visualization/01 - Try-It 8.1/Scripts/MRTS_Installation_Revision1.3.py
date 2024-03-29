import mysql.connector
import easygui
import pandas as pd
import os
import yaml

# Prompt user to select the .yaml configuration file
config_path = easygui.fileopenbox(title="Select your database configuration file", filetypes=['*.yaml'])

# Load MySQL configuration from the selected yaml file
with open(config_path, 'r') as f:
    db = yaml.safe_load(f)

# Extracting connection details from the configuration file
config = {
    'user':     db['user'],
    'password': db['pwrd'],
    'host':     db['host'],
    'auth_plugin': 'mysql_native_password'
}

# Connect to MySQL to check if the database exists
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Create the 'mrts' database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS mrts")

# Close the initial connection
cursor.close()
cnx.close()

# Specify the 'mrts' database for subsequent connections
config['database'] = 'mrts'
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Create necessary tables if they don't exist
# Create NAIC_Codes table
cursor.execute("""
CREATE TABLE IF NOT EXISTS NAIC_Codes (
    NAIC_Code_ID INT AUTO_INCREMENT PRIMARY KEY,
    NAIC_Code INT UNIQUE,
    Business_Type VARCHAR(255)
)
""")

# Create Monthly_Data table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Monthly_Data (
    Data_ID INT AUTO_INCREMENT PRIMARY KEY,
    NAIC_Code_ID INT,
    Year INT,
    Month INT CHECK (Month BETWEEN 1 AND 12),
    Value DECIMAL(10,2),
    FOREIGN KEY (NAIC_Code_ID) REFERENCES NAIC_Codes(NAIC_Code_ID)
)
""")

# Prompt user to select directory containing CSV files
folder_path = easygui.diropenbox(title="Select a folder containing CSV files")

# Helper functions for database interactions
def get_naic_code_id(cursor, code):
    cursor.execute("SELECT NAIC_Code_ID FROM NAIC_Codes WHERE NAIC_Code = %s", (code,))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_naic_code_and_type(cursor, code, business_type):
    if pd.isna(code) or code == 'nan':
        return None
    cursor.execute("INSERT INTO NAIC_Codes (NAIC_Code, Business_Type) VALUES (%s, %s) ON DUPLICATE KEY UPDATE NAIC_Code = VALUES(NAIC_Code), Business_Type = VALUES(Business_Type)", (code, business_type))
    return get_naic_code_id(cursor, code)

def sanitize_value(value):
    if value in ['(NA)', '(S)'] or pd.isna(value):
        return '0'
    return value

# Check if a folder path was selected
if folder_path:
    # Extract all CSV files from the selected directory
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for csv_file in csv_files:
        full_path = os.path.join(folder_path, csv_file)

        # Extract year from the filename
        try:
            year = int(csv_file.split('_')[-1].replace('.csv', ''))
        except ValueError:
            print(f"Skipped {csv_file} due to unexpected file naming format.")
            continue

        data = pd.read_csv(full_path)

        # Populate the database using CSV data
        for index, row in data.iterrows():
            naic_code = row[0]
            business_type = row[1]
            naic_code_id = insert_naic_code_and_type(cursor, naic_code, business_type)

            for month, value in enumerate(row[2:], 1):
                cursor.execute("INSERT INTO Monthly_Data (NAIC_Code_ID, Year, Month, Value) VALUES (%s, %s, %s, %s)", (naic_code_id, year, month, sanitize_value(value)))

            print(f"Inserted data from {csv_file}")

# Commit changes and close connection
cnx.commit()
cursor.close()
cnx.close()

print("Database and tables have been created and populated successfully!")
