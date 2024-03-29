import mysql.connector
import easygui
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
    'database': 'mrts',
    'auth_plugin': 'mysql_native_password'
}

# Connecting to the 'mrts' database
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Validation 1: Count of NAIC Codes
cursor.execute("SELECT COUNT(*) FROM NAIC_Codes")
naic_count = cursor.fetchone()[0]
print(f"Count of NAIC Codes: {naic_count}")
print(f"Count of NAIC Codes in Excel Workbook: 56")

# Validation 2: Monthly Data without Corresponding NAIC Code
cursor.execute("""
SELECT COUNT(*)
FROM Monthly_Data
WHERE NAIC_Code_ID NOT IN (SELECT NAIC_Code_ID FROM NAIC_Codes)
""")
orphan_data_count = cursor.fetchone()[0]
print(f"\nData entries without a corresponding NAIC Code: {orphan_data_count}")

# Validation 3: Monthly Data Range
cursor.execute("""
SELECT COUNT(*)
FROM Monthly_Data
WHERE month NOT BETWEEN 1 AND 12
""")
invalid_month_count = cursor.fetchone()[0]
print(f"\nData entries with an invalid month value: {invalid_month_count}")

# Validation 4: Check for Missing Data in the Monthly_Data Table
cursor.execute("""
SELECT Data_ID, NAIC_Code_ID, year, month, value
FROM Monthly_Data
WHERE NAIC_Code_ID IS NULL OR year IS NULL OR month IS NULL OR value IS NULL
""")
missing_data = cursor.fetchall()
print(f"\nData entries with missing values: {len(missing_data)}")
for md in missing_data:
    print(f"Data_ID: {md[0]}, NAIC_Code_ID: {md[1]}, year: {md[2]}, month: {md[3]}, value: {md[4]}")

# Validation 5: Check for Non-numerical Values in the Monthly_Data Table
cursor.execute("""
SELECT Data_ID, value
FROM Monthly_Data
WHERE value REGEXP '[^0-9.]'
""")
non_numerical_values = cursor.fetchall()
print(f"\nData entries with non-numerical values: {len(non_numerical_values)}")
for nnv in non_numerical_values:
    print(f"Data_ID: {nnv[0]}, value: {nnv[1]}")

# Close the database connection
cursor.close()
cnx.close()
