import mysql.connector
import easygui
import pandas as pd
import os
import yaml

# Prompt user to select the .yaml configuration file
config_path = easygui.fileopenbox(title="Select your database configuration file", filetypes=['*.yaml'])

# Load MySQL configuration from the selected yaml file
try:
    with open(config_path, 'r') as f:
        db = yaml.safe_load(f)

    # Validate required fields in the configuration file
    required_fields = ['user', 'pwrd', 'host']
    for field in required_fields:
        if field not in db:
            raise ValueError(f"Missing '{field}' in the configuration file.")

except Exception as e:
    print(f"Error loading MySQL configuration: {str(e)}")
    exit(1)

# Extracting connection details from the configuration file
config = {
    'user': db['user'],
    'password': db['pwrd'],
    'host': db['host'],
    'auth_plugin': 'mysql_native_password'
}

# Connect to MySQL to check if the database exists
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Create the 'mrts' database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS mrts")

except mysql.connector.Error as err:
    print(f"MySQL error: {err}")
    if 'cnx' in locals() and cnx.is_connected():
        cursor.close()
        cnx.close()
    exit(1)

# Close the initial connection
cursor.close()
cnx.close()

# Specify the 'mrts' database for subsequent connections
config['database'] = 'mrts'
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# SQL Table Creation and Data Insertion
try:
    # Create a table to map group names to NAIC Codes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS NAIC_Groups (
        Group_ID INT AUTO_INCREMENT PRIMARY KEY,
        Group_Name VARCHAR(255) UNIQUE
    )
    """)

    # Create a table to store the relationships between groups and NAIC Codes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS NAIC_Group_Mapping (
        Mapping_ID INT AUTO_INCREMENT PRIMARY KEY,
        Group_ID INT,
        NAIC_Code INT,
        FOREIGN KEY (Group_ID) REFERENCES NAIC_Groups(Group_ID),
        FOREIGN KEY (NAIC_Code) REFERENCES NAIC_Codes(NAIC_Code)
    )
    """)

    # Insert data for the "Retail and Food Services Category" group
    cursor.execute("INSERT INTO NAIC_Groups (Group_Name) VALUES ('Retail and Food Services')")

    # Insert NAIC Codes associated with the "Retail and Food Services Category" group
    cursor.executemany("INSERT INTO NAIC_Group_Mapping (Group_ID, NAIC_Code) VALUES (%s, %s)",
                        [(1, '441'), (1, '442'), (1, '443'), (1, '444'), (1, '445'), (1, '446'),
                         (1, '447'), (1, '448'), (1, '451'), (1, '452'), (1, '453'), (1, '454'),
                         (1, '722')])

    # Insert data for the "Retail sales and food services excl motor vehicle and parts" group
    cursor.execute("INSERT INTO NAIC_Groups (Group_Name) VALUES ('Retail sales and food services excl motor vehicle and parts')")

    # Insert NAIC Codes associated with the "Retail sales and food services excl motor vehicle and parts" group
    cursor.executemany("INSERT INTO NAIC_Group_Mapping (Group_ID, NAIC_Code) VALUES (%s, %s)",
                        [(2, '442'), (2, '443'), (2, '444'), (2, '445'), (2, '446'), (2, '447'),
                         (2, '448'), (2, '451'), (2, '452'), (2, '453'), (2, '454'), (2, '722')])

    # Insert data for the "Retail sales and food services excl gasoline stations" group
    cursor.execute("INSERT INTO NAIC_Groups (Group_Name) VALUES ('Retail sales and food services excl gasoline stations')")

    # Insert NAIC Codes associated with the "Retail sales and food services excl gasoline stations" group
    cursor.executemany("INSERT INTO NAIC_Group_Mapping (Group_ID, NAIC_Code) VALUES (%s, %s)",
                        [(3, '441'), (3, '442'), (3, '443'), (3, '444'), (3, '445'), (3, '446'),
                         (3, '448'), (3, '451'), (3, '452'), (3, '453'), (3, '454'), (3, '722')])

    # Insert data for the "Retail sales and food services excl motor vehicle and parts and gasoline stations" group
    cursor.execute("INSERT INTO NAIC_Groups (Group_Name) VALUES ('Retail sales and food services excl motor vehicle and parts and gasoline stations')")

    # Insert NAIC Codes associated with the "Retail sales and food services excl motor vehicle and parts and gasoline stations" group
    cursor.executemany("INSERT INTO NAIC_Group_Mapping (Group_ID, NAIC_Code) VALUES (%s, %s)",
                        [(4, '442'), (4, '443'), (4, '444'), (4, '445'), (4, '446'), (4, '448'),
                         (4, '451'), (4, '452'), (4, '453'), (4, '454'), (4, '722')])

    # Insert data for the "Retail sales" group
    cursor.execute("INSERT INTO NAIC_Groups (Group_Name) VALUES ('Retail sales')")

    # Insert NAIC Codes associated with the "Retail sales" group
    cursor.executemany("INSERT INTO NAIC_Group_Mapping (Group_ID, NAIC_Code) VALUES (%s, %s)",
                        [(5, '441'), (5, '442'), (5, '443'), (5, '444'), (5, '445'), (5, '446'),
                         (5, '447'), (5, '448'), (5, '451'), (5, '452'), (5, '453'), (5, '454')])

    # Insert data for the "Retail sales (excl. motor vehicle and parts dealers)" group
    cursor.execute("INSERT INTO NAIC_Groups (Group_Name) VALUES ('Retail sales (excl. motor vehicle and parts dealers)')")

    # Insert NAIC Codes associated with the "Retail sales (excl. motor vehicle and parts dealers)" group
    cursor.executemany("INSERT INTO NAIC_Group_Mapping (Group_ID, NAIC_Code) VALUES (%s, %s)",
                        [(6, '442'), (6, '443'), (6, '444'), (6, '445'), (6, '446'), (6, '447'),
                         (6, '448'), (6, '451'), (6, '452'), (6, '453'), (6, '454')])

    # Insert data for the "GAFO(1)" group
    cursor.execute("INSERT INTO NAIC_Groups (Group_Name) VALUES ('GAFO(1)')")

    # Insert NAIC Codes associated with the "GAFO(1)" group
    cursor.executemany("INSERT INTO NAIC_Group_Mapping (Group_ID, NAIC_Code) VALUES (%s, %s)",
                        [(7, '442'), (7, '443'), (7, '448'), (7, '451'), (7, '452'), (7, '4532')])

    # Commit changes and close connection
    cnx.commit()
    cursor.close()
    cnx.close()

    print("Database and tables have been created and populated successfully!")

except mysql.connector.Error as err:
    print(f"MySQL error: {err}")
    if 'cnx' in locals() and cnx.is_connected():
        cursor.close()
        cnx.close()
    exit(1)
