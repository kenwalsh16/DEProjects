## Module 8: ETL, Analysis, and Visualization of the Monthly Retail Trade Survey Data 

This folder contains the project folders, files and documentation for "ETL, Analysis, and Visualization" project completed for Module 8 of the MIT xPRO Professional Certificate in Data Engineering. There are two folders, the first deals with the ETL part of the project, and the second the remainder of the requirements.

**Project Description**

The project focused on data analysis using the Monthly Retail Trade Survey (MRTS) dataset. The aim is to guide you through the steps I used to prepare and analyze the MRTS dataset. Leveraging the insights provided in Video 8.2, I follow a series of steps designed to familiarize the student with the dataset, make necessary data modifications, and export it for analysis. By following along, you'll gain hands-on experience in data manipulation using Excel macros, CSV file handling in Python, and SQL installation script creation. This was the methodology I followed for the project, however, I am sure there are much more efficient and eloquent solutions for all parts of this project.

**Project Goals**

* Project Part One

For part 1 of the project, these were the goals:

* Familiarization: Gain a thorough understanding of the MRTS dataset and its contents by conducting online research and exploring its intricacies. This foundational step will facilitate project development and analysis.

* Modification Planning: Decide on the necessary modifications to be made to the database for optimal analysis readiness. While some modifications are suggested, participants are encouraged to devise additional enhancements tailored to their project goals.

* Data Selection and Export: Determine the specific data elements to retain from the MRTS dataset and export them into a CSV format for further processing and analysis.

* Sample Data Creation: Utilize a text editor to generate sample data in CSV format, ensuring a minimum of four columns and six rows. Participants have the freedom to populate this dataset with any relevant entries of their choice.

* Python Scripting and Verification: Develop a Python script to read the sample data CSV file and validate its readability using the Terminal window. This step reinforces understanding of CSV file handling in Python and ensures proficiency in data retrieval.

* MRTS Dataset Handling: Write a Python script to read the CSV file containing the selected data from the MRTS dataset, and confirm its accessibility through the Terminal window. This task reinforces comprehension of dataset manipulation and retrieval techniques.

* SQL Script Creation: Utilize knowledge acquired from Module 6 to generate an SQL installation script tailored for the MRTS CSV file. This script will facilitate seamless integration of the dataset into a relational database environment, enhancing accessibility and analysis capabilities.

**Project Files**

* CSVs Folder: A folder containing all of the csv files created from the dataset, separated into yearly data
* Images Folder: A folder containing a database schema design image and various images indicting successful running of the different scripts
* Scripts Folder:
  * `Database_Validation.py`: This script file does some basic validation of the database as it is build.
    * Validation 1: Count of NAIC Codes: Queries the 'NAIC_Codes' table for the count of records.
    * Validation 2: Monthly Data without Corresponding NAIC Code: Checks for orphan data entries in the 'Monthly_Data' table.
    * Validation 3: Monthly Data Range: Ensures that the 'month' column in 'Monthly_Data' table has valid month values (1-12).
    * Validation 4: Check for Missing Data: Retrieves data entries with missing values from 'Monthly_Data' table.
    * Validation 5: Check for Non-numerical Values: Retrieves data entries with non-numerical values in the 'value' column from 'Monthly_Data' table.
  * `Easygui Import - Sample.py`: This script facilitates the selection and reading of a CSV file, allowing users to quickly view its contents.
  * `Export_CSVs - xlrd.py`: This script converts each worksheet from an Excel workbook into separate CSV files.
  * `MRTS_Installation_Revision1.3.py`: This is the main script, it creates a MySQL database and tables for storing data related to NAIC codes and monthly data. It prompts the user to select a YAML configuration file containing database credentials, connects to MySQL to check and create the database if it doesn't exist, and then creates tables for NAIC codes and monthly data. Additionally, it allows the user to select a directory containing CSV files, extracts data from these files, and populates the database tables accordingly. Finally, it commits the changes and closes the database connection.
  * `db.yaml`: An example db.yaml file for the database connection
* `test.csv`: A NAICs code test file
* `Try-It 8.1.ipynb`: A Jupyter notebook project file detailing the project and results.

* Project Part Two

For part 2 of the project, these were the goals:

* Write at least two SQL queries directly in MySQL Workbench to initiate analysis of the MRTS database and validate the expected output.

* Test the execution of the queries on the database from the Terminal window using Python, following the methodology demonstrated in Video 8.3.

* Develop multiple SQL queries to analyze the MRTS dataset based on the instructions provided in the videos. These queries should aim to:
    
    * Investigate the trend of total sales for retail and food services categories, exploring adjustments to enhance visualization clarity.
    * Compare trends among businesses such as bookstores, sporting goods stores, and hobbies, toys, and games stores, identifying the fastest-growing entity, seasonal patterns, and changes in 2020.
    * Examine the relationship between women's clothing and men's clothing businesses, analyzing percentage changes and their contribution to the overall dataset over time.

* Craft queries to analyze and generate graphical representations of rolling time windows for at least two selected businesses within the dataset.

**Project Files**

* CSVs Folder: A folder containing all of the csv files created from the dataset, separated into yearly data
* Images Folder: A folder containing a database schema design image and various images indicting successful running of the different scripts
* `Data Formatting Macro.txt`: This macro is designed to perform various data cleaning tasks on multiple worksheets within an Excel workbook. Here's a brief explanation of what each task accomplishes:
    * Deletes the first three rows of each worksheet.
    * Copies the content of cells A1 and B1 to cells A2 and B2 to create a row of header columns.
    * Deletes the empty row at the top of each worksheet.
    * Deletes rows 2 through 9 on each worksheet.
    * Removes specific rows (3 and 8) which are identified as aggregate rows and not required.
    * Resolves an issue by replacing the value in cell A57 with a predefined value (722513).
    * Deletes column P from each worksheet to remove spurious data.
    * Deletes unnecessary columns based on specified column names and criteria:
        a. Deletes columns with names specified in the "colName" array.
        b. Deletes rows starting from the occurrence of "ADJUSTED(2)" until the first occurrence of two consecutive empty rows.
* `Export_CSVs - xlrd.py`: This script converts each worksheet from an Excel workbook into separate CSV files.
* `MRTS_Installation_Revision1.3.py`: This is the main script, it creates a MySQL database and tables for storing data related to NAIC codes and monthly data. It prompts the user to select a YAML configuration file containing database credentials, connects to MySQL to check and create the database if it doesn't exist, and then creates tables for NAIC codes and monthly data. Additionally, it allows the user to select a directory containing CSV files, extracts data from these files, and populates the database tables accordingly. Finally, it commits the changes and closes the database connection.
* `Additional_Tables-Installation_Category_Associations_Table.py`: This script creates and populates additional required MySQL database tables to map group names to NAIC codes for retail categories.
* `Visualization Script.py`: This script contains the SQL Code performed to carry out the requirements of the project as outlined in the project jupyter notebook.
* `Additional Rolling Time Business.py`: This script runs sql code for two queries related to specific business questions outlined in the project.
  * Query 1: This query retrieves rolling sum, rolling average, rolling growth rate, rolling minimum, and rolling maximum values for the retail sales of sporting goods stores. It calculates these metrics over time (year and month) for the specified business type. The results are ordered by year and month.
  * Query 2: This query calculates aggregated data for total monthly sales and sales from 3, 6, 9, and 12 months ago for sporting goods stores. It utilizes window functions to compute the total sales over specified rolling time windows. The results are ordered by year and month for visualization.
* `Project8.ipnyb`: A Jupyter notebook project file detailing the project and results.  