import mysql.connector
import easygui
import yaml
import matplotlib.pyplot as plt

def load_mysql_config(config_path):
    try:
        with open(config_path, 'r') as f:
            db = yaml.safe_load(f)
            required_keys = ['user', 'pwrd', 'host']
            
            if all(key in db for key in required_keys):
                return {
                    'user': db['user'],
                    'password': db['pwrd'],
                    'host': db['host'],
                    'auth_plugin': 'mysql_native_password',
                    'database': 'mrts'  # Specify the 'mrts' database here
                }
            else:
                raise ValueError("Invalid MySQL configuration file. Missing required keys.")
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file not found.")
    except yaml.YAMLError:
        raise ValueError("Invalid YAML format in the configuration file.")

def check_database_existence(cursor):
    cursor.execute("SHOW DATABASES LIKE 'mrts'")
    return cursor.fetchone() is not None

def main():
    try:
        # Prompt user to select the .yaml configuration file
        config_path = easygui.fileopenbox(title="Select your database configuration file", filetypes=['*.yaml'])
        
        # Load MySQL configuration from the selected yaml file
        config = load_mysql_config(config_path)

        # Connect to MySQL to check if the database exists
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        if not check_database_existence(cursor):
            # Database does not exist
            print("Database does not exist, please run the installation script")
        else:
            # Database exists, proceed with the rest of the script

# Insert SQL Code Here:
            # Q3D3: SQL Query for Sporting Goods Stores only
            sql_query = """
            SELECT
                Business_Type,
                Year,
                Month,
                Rolling_Sum,
                Rolling_Average,
                Rolling_Growth_Rate,
                Rolling_Min,
                Rolling_Max
            FROM (
                SELECT
                    NC.Business_Type,
                    MD.Year,
                    MD.Month,
                    SUM(MD.Value) AS Rolling_Sum,
                    AVG(MD.Value) AS Rolling_Average,
                    (SUM(MD.Value) - LAG(SUM(MD.Value), 1) OVER (PARTITION BY NC.Business_Type, MD.Year ORDER BY MD.Month)) / LAG(SUM(MD.Value), 1) OVER (PARTITION BY NC.Business_Type, MD.Year ORDER BY MD.Month) AS Rolling_Growth_Rate,
                    MIN(MD.Value) AS Rolling_Min,
                    MAX(MD.Value) AS Rolling_Max
                FROM
                    NAIC_Codes NC
                JOIN
                    Monthly_Data MD ON NC.NAIC_Code_ID = MD.NAIC_Code_ID
                WHERE
                    NC.Business_Type = 'Sporting Goods Stores' -- Direct filter for Sporting Goods Stores
                GROUP BY
                    NC.Business_Type,
                    MD.Year,
                    MD.Month
            ) AS Subquery
            ORDER BY
                Year,
                Month;
            """

            cursor.execute(sql_query)
            rows = cursor.fetchall()

            # Assuming the "Sporting Goods Stores" exists, there will only be one group's data
            # Unpack the fetched data for plotting
            year_months, rolling_sums, rolling_averages = zip(*[(f"{row[1]}-{str(row[2]).zfill(2)}", row[3], row[4]) for row in rows])

            # Extract unique years from the dates
            unique_years = sorted(set(date.split('-')[0] for date in year_months))

            # Plot the data
            plt.figure(figsize=(14, 8))
            plt.plot(year_months, rolling_sums, label='Sporting Goods Stores Rolling Sum')
            plt.plot(year_months, rolling_averages, label='Sporting Goods Stores Rolling Average', linestyle='--')

            plt.xlabel('Year')
            plt.ylabel('Values')
            plt.title('Q3D3 - Rolling Sum and Average for Sporting Goods Stores')
            plt.legend()

            # Set xticks to only the unique years, positioning them at the start of each year (assuming January data is present)
            plt.xticks([f"{year}-01" for year in unique_years], unique_years)

            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        # Q3D4: Modified SQL Query for Sporting Goods Stores only
        sql_query = """
            WITH RollingWindow3Months AS (
                SELECT
                    NAIC_Code_ID,
                    Year,
                    Month,
                    SUM(Value) AS TotalValue,
                    LAG(SUM(Value), 3) OVER (ORDER BY Year, Month) AS TotalValue_3MonthsAgo
                FROM Monthly_Data
                GROUP BY NAIC_Code_ID, Year, Month
            ),
            RollingWindow6Months AS (
                SELECT
                    NAIC_Code_ID,
                    Year,
                    Month,
                    SUM(Value) AS TotalValue,
                    LAG(SUM(Value), 6) OVER (ORDER BY Year, Month) AS TotalValue_6MonthsAgo
                FROM Monthly_Data
                GROUP BY NAIC_Code_ID, Year, Month
            ),
            RollingWindow9Months AS (
                SELECT
                    NAIC_Code_ID,
                    Year,
                    Month,
                    SUM(Value) AS TotalValue,
                    LAG(SUM(Value), 9) OVER (ORDER BY Year, Month) AS TotalValue_9MonthsAgo
                FROM Monthly_Data
                GROUP BY NAIC_Code_ID, Year, Month
            ),
            RollingWindow12Months AS (
                SELECT
                    NAIC_Code_ID,
                    Year,
                    Month,
                    SUM(Value) AS TotalValue,
                    LAG(SUM(Value), 12) OVER (ORDER BY Year, Month) AS TotalValue_12MonthsAgo
                FROM Monthly_Data
                GROUP BY NAIC_Code_ID, Year, Month
            ),
            FilteredNAICCodes AS (
                SELECT NAIC_Code_ID
                FROM NAIC_Codes
                WHERE Business_Type = 'Sporting Goods Stores' -- Changed to filter based on the Business_Type field
            ),
            AggregatedData AS (
                SELECT
                    M.Year,
                    M.Month,
                    SUM(M.Value) AS TotalMonthlySales,
                    SUM(R3.TotalValue_3MonthsAgo) AS TotalSales_3MonthsAgo,
                    SUM(R6.TotalValue_6MonthsAgo) AS TotalSales_6MonthsAgo,
                    SUM(R9.TotalValue_9MonthsAgo) AS TotalSales_9MonthsAgo,
                    SUM(R12.TotalValue_12MonthsAgo) AS TotalSales_12MonthsAgo
                FROM Monthly_Data M
                JOIN FilteredNAICCodes FNC ON M.NAIC_Code_ID = FNC.NAIC_Code_ID
                LEFT JOIN RollingWindow3Months R3 ON M.NAIC_Code_ID = R3.NAIC_Code_ID AND M.Year = R3.Year AND M.Month = R3.Month
                LEFT JOIN RollingWindow6Months R6 ON M.NAIC_Code_ID = R6.NAIC_Code_ID AND M.Year = R6.Year AND M.Month = R6.Month
                LEFT JOIN RollingWindow9Months R9 ON M.NAIC_Code_ID = R9.NAIC_Code_ID AND M.Year = R9.Year AND M.Month = R9.Month
                LEFT JOIN RollingWindow12Months R12 ON M.NAIC_Code_ID = R12.NAIC_Code_ID AND M.Year = R12.Year AND M.Month = R12.Month
                GROUP BY M.Year, M.Month
            )
            SELECT
                Year,
                Month,
                TotalMonthlySales,
                TotalSales_3MonthsAgo,
                TotalSales_6MonthsAgo,
                TotalSales_9MonthsAgo,
                TotalSales_12MonthsAgo
            FROM AggregatedData
            ORDER BY Year, Month;
            """
        
        # Execute the SQL query and fetch the data
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Initialize lists to hold the X-axis labels and the different Y-axis data
        x_labels = []
        total_monthly_sales = []
        total_sales_3_months_ago = []
        total_sales_6_months_ago = []
        total_sales_9_months_ago = []
        total_sales_12_months_ago = []

        # Populate the lists with data from 'rows'
        for row in rows:
            year, month, monthly_sales, sales_3mo, sales_6mo, sales_9mo, sales_12mo = row
            x_labels.append(f"{year}-{str(month).zfill(2)}")
            total_monthly_sales.append(monthly_sales)
            total_sales_3_months_ago.append(sales_3mo)
            total_sales_6_months_ago.append(sales_6mo)
            total_sales_9_months_ago.append(sales_9mo)
            total_sales_12_months_ago.append(sales_12mo)

        # Extract unique years from the dates
        unique_years = sorted(set(label.split('-')[0] for label in x_labels))

        # Plotting the data
        plt.figure(figsize=(14, 8))

        # Plot total monthly sales
        plt.plot(x_labels, total_monthly_sales, label='Total Monthly Sales')

        # Optionally, plot the sales from 3, 6, 9, and 12 months ago if needed
        plt.plot(x_labels, total_sales_3_months_ago, label='Sales 3 Months Ago')
        plt.plot(x_labels, total_sales_6_months_ago, label='Sales 6 Months Ago')
        plt.plot(x_labels, total_sales_9_months_ago, label='Sales 9 Months Ago')
        plt.plot(x_labels, total_sales_12_months_ago, label='Sales 12 Months Ago')

        # Adding labels and title
        plt.xlabel('Year-Month')
        plt.ylabel('Sales')
        plt.title('Q3D2 - Monthly Total Sales for Sporting Goods Stores')

        # Customizing the plot
        plt.legend()

        # Set xticks to only the unique years, positioning them at the start of each year
        # Assuming the data contains January for all the years which you would want to use as the tick mark
        plt.xticks([f"{year}-01" for year in unique_years], unique_years)

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show the plot
        plt.show()

    except mysql.connector.Error as err:
        # Handle MySQL errors (e.g., connection issues)
        print(f"MySQL Error: {err}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()

if __name__ == "__main__":
    main()
