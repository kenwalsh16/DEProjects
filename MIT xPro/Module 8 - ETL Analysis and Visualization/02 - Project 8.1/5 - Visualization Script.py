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
    cnx = None  # Initialize connection outside of try block
    cursor = None  # Initialize cursor outside of try block
    
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

            # Q3A1: Run SQL Statement for time series plot
            sql = """
            SELECT 
                CONCAT(Monthly_Data.Year, '-', LPAD(Monthly_Data.Month, 2, '0'), '-01') AS date_formatted, 
                CAST(SUM(Monthly_Data.Value) AS UNSIGNED) AS sales
            FROM 
                Monthly_Data 
            JOIN 
                NAIC_Codes ON Monthly_Data.NAIC_Code_ID = NAIC_Codes.NAIC_Code_ID
            JOIN
                NAIC_Group_Mapping ON NAIC_Codes.NAIC_Code = NAIC_Group_Mapping.NAIC_Code
            JOIN
                NAIC_Groups ON NAIC_Group_Mapping.Group_ID = NAIC_Groups.Group_ID
            WHERE 
                NAIC_Groups.Group_Name = 'Retail and Food Services'
            GROUP BY 
                Monthly_Data.Year, Monthly_Data.Month
            ORDER BY 
                ABS(Monthly_Data.Year - 2021), Monthly_Data.Year DESC, Monthly_Data.Month DESC;
            """

            cursor.execute(sql)

            month = []
            sales = []

            # Print all the first cells for all of the rows
            for row in cursor.fetchall():
                month.append(row[0])
                sales.append(row[1])

            # Extract unique years from the data
            unique_years = set(date.split('-')[0] for date in month)

            # Plot as a time series with year separators on the x-axis
            plt.figure(figsize=(14, 8))
            plt.plot(month[::-1], sales[::-1])  # Reverse the lists to change direction
            plt.title("Q3A1 - Retail and Food Services Monthly Totals")  # Title
            plt.xlabel("Years")  # X-axis label
            plt.ylabel("Sales")  # Y-axis label
            plt.xticks([f"{year}-01-01" for year in sorted(unique_years, reverse=True)], sorted(unique_years, reverse=True), rotation=45)
            plt.tight_layout()  # Ensure labels fit in the plot area
            plt.show()

            # Q3A1a: Run SQL Statement for moving averages
            moving_avg_sql = """
            WITH MovingAverages AS (
                SELECT
                    Monthly_Data.Year,
                    Monthly_Data.Month,
                    SUM(Monthly_Data.Value) AS TotalSales,
                    AVG(SUM(Monthly_Data.Value)) OVER (ORDER BY Monthly_Data.Year, Monthly_Data.Month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS ThreeMonthAvg,
                    AVG(SUM(Monthly_Data.Value)) OVER (ORDER BY Monthly_Data.Year, Monthly_Data.Month ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS SixMonthAvg,
                    AVG(SUM(Monthly_Data.Value)) OVER (ORDER BY Monthly_Data.Year, Monthly_Data.Month ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS TwelveMonthAvg
                FROM
                    Monthly_Data
                JOIN 
                    NAIC_Codes ON Monthly_Data.NAIC_Code_ID = NAIC_Codes.NAIC_Code_ID
                JOIN
                    NAIC_Group_Mapping ON NAIC_Codes.NAIC_Code = NAIC_Group_Mapping.NAIC_Code
                JOIN
                    NAIC_Groups ON NAIC_Group_Mapping.Group_ID = NAIC_Groups.Group_ID
                WHERE
                    NAIC_Groups.Group_Name = 'Retail and Food Services'
                GROUP BY
                    Monthly_Data.Year, Monthly_Data.Month
            )
            SELECT
                Year,
                Month,
                TotalSales,
                ThreeMonthAvg,
                SixMonthAvg,
                TwelveMonthAvg
            FROM
                MovingAverages
            ORDER BY
                Year, Month;
            """

            cursor.execute(moving_avg_sql)

            # Initialize lists to store moving average data
            ma_dates = []
            ma_3months = []
            ma_6months = []
            ma_12months = []

            # Fetch and process the moving average data
            for row in cursor.fetchall():
                ma_dates.append(f"{row[0]}-{row[1]:02d}")
                ma_3months.append(row[3])
                ma_6months.append(row[4])
                ma_12months.append(row[5])

            # Plot moving averages
            plt.figure(figsize=(14, 8))
            plt.plot(ma_dates, ma_3months, label='3-Month Avg')
            plt.plot(ma_dates, ma_6months, label='6-Month Avg')
            plt.plot(ma_dates, ma_12months, label='12-Month Avg')
            plt.title("Q3A1a - Retail and Food Services Moving Averages")  # Title
            plt.xlabel("Years")  # X-axis label
            plt.ylabel("Sales")  # Y-axis label
            # Adjust the x-axis tick positions and labels
            tick_positions = list(range(0, len(ma_dates), len(unique_years)))
            tick_labels = [ma_dates[i] for i in tick_positions]

            plt.xticks(tick_positions, tick_labels, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()

            # Q3A1b - Run SQL Statement for Quarterly Sales of 'Retail and Food Services' NAIC group
            quarterly_sales_sql = """
            WITH QuarterlySales AS (
                SELECT
                    md.Year AS Year,
                    CASE
                        WHEN md.Month BETWEEN 1 AND 3 THEN 'Q1'
                        WHEN md.Month BETWEEN 4 AND 6 THEN 'Q2'
                        WHEN md.Month BETWEEN 7 AND 9 THEN 'Q3'
                        WHEN md.Month BETWEEN 10 AND 12 THEN 'Q4'
                    END AS Quarter,
                    SUM(md.Value) AS QuarterlyTotal
                FROM
                    Monthly_Data md
                JOIN
                    NAIC_Codes nc ON md.NAIC_Code_ID = nc.NAIC_Code_ID
                JOIN
                    NAIC_Group_Mapping ngm ON nc.NAIC_Code = ngm.NAIC_Code
                JOIN
                    NAIC_Groups ng ON ngm.Group_ID = ng.Group_ID
                WHERE
                    ng.Group_Name = 'Retail and Food Services'
                GROUP BY
                    md.Year, Quarter
            )
            SELECT
                Year,
                Quarter,
                SUM(QuarterlyTotal) AS QuarterlySales
            FROM
                QuarterlySales
            GROUP BY
                Year, Quarter
            ORDER BY
                Year, Quarter;
            """

            cursor.execute(quarterly_sales_sql)

            qs_years = []
            qs_quarters = []
            qs_sales = []

            # Fetch and process the quarterly sales data
            for row in cursor.fetchall():
                qs_years.append(row[0])
                qs_quarters.append(row[1])
                qs_sales.append(row[2])

            # Extract unique years from the data
            unique_years_quarterly = sorted(set(qs_years))

            # Create an empty list for quarterly sales corresponding to each unique year
            qs_sales_by_year = [0] * len(unique_years_quarterly)

            # Populate the quarterly sales data in the correct positions
            for year, quarter, sales in zip(qs_years, qs_quarters, qs_sales):
                year_index = unique_years_quarterly.index(year)
                if quarter == 'Q1':
                    qs_sales_by_year[year_index] += sales
                elif quarter == 'Q2':
                    qs_sales_by_year[year_index] += sales
                elif quarter == 'Q3':
                    qs_sales_by_year[year_index] += sales
                elif quarter == 'Q4':
                    qs_sales_by_year[year_index] += sales

            # Plot Quarterly Sales as a time series with years on the x-axis
            plt.figure(figsize=(14, 8))
            plt.plot(unique_years_quarterly, qs_sales_by_year, marker='o', linestyle='-', label='Quarterly Sales')
            plt.title("Q3A1b - Retail and Food Services Quarterly Sales")  # Title
            plt.xlabel("Years")  # X-axis label
            plt.ylabel("Sales")  # Y-axis label
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

            # Q3B1: First SQL query for total sales
            cursor.execute("""
                SELECT
                    NC.Business_Type,
                    SUM(MD.Value) AS TotalSales
                FROM
                    Monthly_Data MD
                JOIN
                    NAIC_Codes NC ON MD.NAIC_Code_ID = NC.NAIC_Code_ID
                WHERE
                    NC.Business_Type IN ('Book stores', 'Sporting Goods Stores', 'Hobby, Toy, and Game Stores')
                GROUP BY
                    NC.Business_Type
                ORDER BY
                    TotalSales DESC;
            """)
            results = cursor.fetchall()
            business_types = [result[0] for result in results]
            sales = [result[1] for result in results]

            # Set the size of the plot
            plt.figure(figsize=(14, 8))

            # Create the bar plot
            plt.bar(business_types, sales)

            # Set the title and labels
            plt.title('Q3B1 - Total Sales by Business Type')
            plt.xlabel('Business Type')
            plt.ylabel('Total Sales')

            # Display the plot
            plt.show()

            # Q3B2 - Second SQL query for yearly growth rate
            cursor.execute("""
                WITH YearlySales AS (
                    SELECT
                        NC.Business_Type,
                        MD.Year,
                        SUM(MD.Value) AS TotalSales,
                        LAG(SUM(MD.Value)) OVER(PARTITION BY NC.Business_Type ORDER BY MD.Year) AS PrevTotalSales
                    FROM
                        Monthly_Data MD
                    JOIN
                        NAIC_Codes NC ON MD.NAIC_Code_ID = NC.NAIC_Code_ID
                    WHERE
                        MD.Year BETWEEN 1992 AND 2020
                        AND NC.Business_Type IN ('Book stores', 'Sporting Goods Stores', 'Hobby, Toy, and Game Stores')
                    GROUP BY
                        NC.Business_Type, MD.Year
                )
                
                SELECT
                    Business_Type,
                    Year,
                    CASE 
                        WHEN PrevTotalSales = 0 OR PrevTotalSales IS NULL THEN NULL
                        ELSE (TotalSales - PrevTotalSales) / PrevTotalSales * 100
                    END AS GrowthRate
                FROM
                    YearlySales
                WHERE 
                    PrevTotalSales IS NOT NULL
                ORDER BY 
                    Business_Type, 
                    Year;
            """)
            growth_results = cursor.fetchall()

            # Extract the data into usable format for plotting
            years = list(set(row[1] for row in growth_results))
            years.sort()

            business_types_growth = list(set(row[0] for row in growth_results))
            growth_data = {business: [] for business in business_types_growth}

            for row in growth_results:
                business, year, growth_rate = row
                growth_data[business].append(growth_rate)

            # Set the figure size before any plotting
            plt.figure(figsize=(14, 8))

            # Plot growth rate over years
            for business, growth_rates in growth_data.items():
                plt.plot(years, growth_rates, label=business)

            # Now add the plot elements
            plt.title('Q3B2 - Yearly Growth Rate by Business Type')
            plt.xlabel('Year')
            plt.ylabel('Growth Rate (%)')
            plt.legend(loc="lower left")
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)

            # Make sure the layout is tight so everything fits well
            plt.tight_layout()

            # Finally, display the plot
            plt.show()

            # Q3B3 - SQL query for yearly sales by business type and year
            cursor.execute("""
                SELECT
                    MD.Year,
                    NC.Business_Type,
                    SUM(MD.Value) AS TotalSales
                FROM
                    Monthly_Data MD
                JOIN
                    NAIC_Codes NC ON MD.NAIC_Code_ID = NC.NAIC_Code_ID
                WHERE
                    MD.Year BETWEEN 1992 AND 2020
                    AND NC.Business_Type IN ('Book stores', 'Sporting Goods Stores', 'Hobby, Toy, and Game Stores')
                GROUP BY
                    MD.Year, NC.Business_Type
                ORDER BY
                    NC.Business_Type, MD.Year;
            """)
            yearly_sales_results = cursor.fetchall()
            
            # Extract the data into usable format for plotting
            years = sorted(list(set(row[0] for row in yearly_sales_results)))
            business_types_yearly = list(set(row[1] for row in yearly_sales_results))
            sales_data = {business: [0]*len(years) for business in business_types_yearly}

            # Set the figure size before plotting
            plt.figure(figsize=(14, 8))

            for row in yearly_sales_results:
                year, business, total_sales = row
                idx = years.index(year)
                sales_data[business][idx] = total_sales

            for business, yearly_sales in sales_data.items():
                plt.plot(years, yearly_sales, label=business)

            plt.title('Q3B3 - Yearly Sales by Business Type')
            plt.xlabel('Year')
            plt.ylabel('Total Sales')
            plt.legend(loc="upper left")
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)

            # Ensure the layout is tight so everything fits well
            plt.tight_layout()

            # Display the plot
            plt.show()

            # Q3B4 - SQL query for quarterly sales over time
            cursor.execute("""
                SELECT
                    MD.Year,
                    NC.Business_Type,
                    SUM(CASE 
                        WHEN MD.Month BETWEEN 1 AND 3 THEN MD.Value
                        ELSE 0
                        END) AS Q1_Sales,
                    SUM(CASE 
                        WHEN MD.Month BETWEEN 4 AND 6 THEN MD.Value
                        ELSE 0
                        END) AS Q2_Sales,
                    SUM(CASE 
                        WHEN MD.Month BETWEEN 7 AND 9 THEN MD.Value
                        ELSE 0
                        END) AS Q3_Sales,
                    SUM(CASE 
                        WHEN MD.Month BETWEEN 10 AND 12 THEN MD.Value
                        ELSE 0
                        END) AS Q4_Sales
                FROM
                    Monthly_Data MD
                JOIN
                    NAIC_Codes NC ON MD.NAIC_Code_ID = NC.NAIC_Code_ID
                WHERE
                    MD.Year BETWEEN 1992 AND 2021
                    AND NC.Business_Type IN ('Book stores', 'Sporting Goods Stores', 'Hobby, Toy, and Game Stores')
                GROUP BY
                    MD.Year, NC.Business_Type
                ORDER BY
                    MD.Year, NC.Business_Type;
            """)
            
            quarterly_sales_results = cursor.fetchall()
            
            # Structuring the data for stacked column plotting
            years = sorted(list(set(row[0] for row in quarterly_sales_results)))
            business_types_quarterly = list(set(row[1] for row in quarterly_sales_results))
            
            quarterly_sales_data = {business: {"Q1": [0]*len(years), "Q2": [0]*len(years), "Q3": [0]*len(years), "Q4": [0]*len(years)} for business in business_types_quarterly}
            
            for row in quarterly_sales_results:
                year, business, q1_sales, q2_sales, q3_sales, q4_sales = row
                idx = years.index(year)
                quarterly_sales_data[business]["Q1"][idx] = q1_sales
                quarterly_sales_data[business]["Q2"][idx] = q2_sales
                quarterly_sales_data[business]["Q3"][idx] = q3_sales
                quarterly_sales_data[business]["Q4"][idx] = q4_sales
            
            # Plotting the stacked column chart
            width = 0.35  # Width of the bars
            plt.figure(figsize=(14, 8))
            
            for idx, business in enumerate(business_types_quarterly):
                if idx == 0:
                    bottom = [0] * len(years)
                else:
                    prev_business = business_types_quarterly[idx - 1]
                    bottom = [sum(x) for x in zip(quarterly_sales_data[prev_business]["Q1"], quarterly_sales_data[prev_business]["Q2"], quarterly_sales_data[prev_business]["Q3"], quarterly_sales_data[prev_business]["Q4"])]
                
                plt.bar(years, quarterly_sales_data[business]["Q1"], width, label=f"{business} Q1", bottom=bottom)
                bottom = [a+b for a, b in zip(bottom, quarterly_sales_data[business]["Q1"])]
                
                plt.bar(years, quarterly_sales_data[business]["Q2"], width, label=f"{business} Q2", bottom=bottom)
                bottom = [a+b for a, b in zip(bottom, quarterly_sales_data[business]["Q2"])]
                
                plt.bar(years, quarterly_sales_data[business]["Q3"], width, label=f"{business} Q3", bottom=bottom)
                bottom = [a+b for a, b in zip(bottom, quarterly_sales_data[business]["Q3"])]
                
                plt.bar(years, quarterly_sales_data[business]["Q4"], width, label=f"{business} Q4", bottom=bottom)
            
            plt.title('Q3B4 - Quarterly Sales Over Time by Business Type')
            plt.xlabel('Year')
            plt.ylabel('Quarterly Sales')
            plt.legend(loc="upper left")
            plt.tight_layout()
            plt.show()

            # Q3B5 - SQL query for Sales in 2020 and Average Percentage Increase
            cursor.execute("""
                SELECT
                    NC.Business_Type,
                    SUM(CASE 
                        WHEN MD.Year = 2020 THEN MD.Value
                        ELSE 0
                        END) AS Sales_2020,
                    ROUND(
                        AVG(CASE 
                            WHEN MD.Year <> 2020 THEN (MD.Value - PrevYear.Value) / PrevYear.Value * 100
                            ELSE NULL
                            END), 2
                    ) AS Avg_Percentage_Increase
                FROM
                    Monthly_Data MD
                JOIN
                    NAIC_Codes NC ON MD.NAIC_Code_ID = NC.NAIC_Code_ID
                LEFT JOIN
                    Monthly_Data PrevYear ON MD.NAIC_Code_ID = PrevYear.NAIC_Code_ID AND MD.Year = PrevYear.Year + 1
                WHERE
                    MD.Year BETWEEN 1992 AND 2020
                    AND NC.Business_Type IN ('Book stores', 'Sporting Goods Stores', 'Hobby, Toy, and Game Stores')
                GROUP BY
                    NC.Business_Type
                ORDER BY
                    NC.Business_Type;
            """)
            sales_avg_results = cursor.fetchall()

            # Extract data for plotting
            business_types = [result[0] for result in sales_avg_results]
            sales_2020 = [result[1] for result in sales_avg_results]
            avg_percentage_increase = [result[2] for result in sales_avg_results]

            # Plot the combined bar chart
            fig, ax1 = plt.subplots(figsize=(14, 8))
            
            # Twin the axes
            ax2 = ax1.twinx()
            
            # Plot data
            ax1.bar(business_types, sales_2020, color='g', label="Sales 2020")
            ax2.plot(business_types, avg_percentage_increase, color='b', marker='o', label="Avg % Increase")
            
            # Set the y axis label
            ax1.set_ylabel('Sales 2020', color='g')
            ax2.set_ylabel('Average % Increase', color='b')

            # Title and show the plot
            plt.title('Q3B5 - Sales 2020 and Average Percentage Increase by Business Type')
            fig.tight_layout()
            plt.show()

            # Q3C1 - Clothing Comparisons:
            sql_query = """
            SELECT
                MD.Year,
                SUM(CASE 
                    WHEN NC.Business_Type = "Men's clothing stores" THEN MD.Value
                    ELSE 0
                END) AS Men_Sales,
                SUM(CASE 
                    WHEN NC.Business_Type = "Women's clothing stores" THEN MD.Value
                    ELSE 0
                END) AS Women_Sales,
                (SUM(CASE 
                    WHEN NC.Business_Type = "Men's clothing stores" THEN MD.Value
                    ELSE 0
                END) - SUM(CASE 
                        WHEN NC.Business_Type = "Women's clothing stores" THEN MD.Value
                        ELSE 0
                    END)) / SUM(CASE 
                        WHEN NC.Business_Type = "Women's clothing stores" THEN MD.Value
                        ELSE 0
                    END) * 100 AS Percent_Difference_Men_Women,
                (SUM(CASE 
                    WHEN NC.Business_Type = "Men's clothing stores" THEN MD.Value
                    ELSE 0
                END) - LAG(SUM(CASE 
                        WHEN NC.Business_Type = "Men's clothing stores" THEN MD.Value
                        ELSE 0
                        END), 1) OVER (ORDER BY MD.Year)) / LAG(SUM(CASE 
                            WHEN NC.Business_Type = "Men's clothing stores" THEN MD.Value
                            ELSE 0
                        END), 1) OVER (ORDER BY MD.Year) * 100 AS Percent_Difference_Men_Year,
                (SUM(CASE 
                    WHEN NC.Business_Type = "Women's clothing stores" THEN MD.Value
                    ELSE 0
                END) - LAG(SUM(CASE 
                        WHEN NC.Business_Type = "Women's clothing stores" THEN MD.Value
                        ELSE 0
                        END), 1) OVER (ORDER BY MD.Year)) / LAG(SUM(CASE 
                            WHEN NC.Business_Type = "Women's clothing stores" THEN MD.Value
                            ELSE 0
                        END), 1) OVER (ORDER BY MD.Year) * 100 AS Percent_Difference_Women_Year
            FROM
                Monthly_Data MD
            JOIN
                NAIC_Codes NC ON MD.NAIC_Code_ID = NC.NAIC_Code_ID
            WHERE
                MD.Year BETWEEN 1992 AND 2021
                AND (NC.Business_Type = "Men's clothing stores" OR NC.Business_Type = "Women's clothing stores")
            GROUP BY
                MD.Year
            ORDER BY
                MD.Year;
            """
            cursor.execute(sql_query)
            result = cursor.fetchall()

            # Assuming the result is a list of tuples like [(Year, Men_Sales, Women_Sales), (...), ...]
            years = [row[0] for row in result]
            men_sales = [row[1] for row in result]
            women_sales = [row[2] for row in result]

            # Plotting the results
            plt.figure(figsize=(14, 8))
            plt.plot(years, men_sales, label="Men's Sales")
            plt.plot(years, women_sales, label="Women's Sales")
            plt.xlabel('Year')
            plt.ylabel('Sales')
            plt.title('Q3C1 - Sales Over Years by Gender')
            plt.legend()
            plt.show()

            # Q3D1: SQL Query for Retail and Food Services group only
            sql_query = """
            SELECT
                Group_Name,
                Year,
                Month,
                Rolling_Sum,
                Rolling_Average,
                Rolling_Growth_Rate,
                Rolling_Min,
                Rolling_Max
            FROM (
                SELECT
                    NG.Group_Name,
                    MD.Year,
                    MD.Month,
                    SUM(MD.Value) AS Rolling_Sum,
                    AVG(MD.Value) AS Rolling_Average,
                    (SUM(MD.Value) - LAG(SUM(MD.Value), 1) OVER (PARTITION BY NG.Group_Name, MD.Year ORDER BY MD.Month)) / LAG(SUM(MD.Value), 1) OVER (PARTITION BY NG.Group_Name, MD.Year ORDER BY MD.Month) AS Rolling_Growth_Rate,
                    MIN(MD.Value) AS Rolling_Min,
                    MAX(MD.Value) AS Rolling_Max
                FROM
                    NAIC_Groups NG
                JOIN
                    NAIC_Group_Mapping NGM ON NG.Group_ID = NGM.Group_ID
                JOIN
                    NAIC_Codes NC ON NGM.NAIC_Code = NC.NAIC_Code
                JOIN
                    Monthly_Data MD ON NC.NAIC_Code_ID = MD.NAIC_Code_ID
                WHERE
                    NG.Group_Name = 'Retail and Food Services' -- Filter for the specific group
                GROUP BY
                    NG.Group_Name,
                    MD.Year,
                    MD.Month
            ) AS Subquery;
            """

            cursor.execute(sql_query)
            rows = cursor.fetchall()

            # Assuming the "Retail and Food Services" group exists, there will only be one group's data
            # Unpack the fetched data for plotting
            year_months, rolling_sums, rolling_averages = zip(*[(f"{row[1]}-{str(row[2]).zfill(2)}", row[3], row[4]) for row in rows])

            # Extract unique years from the dates
            unique_years = sorted(set(date.split('-')[0] for date in year_months))

            # Plot the data
            plt.figure(figsize=(14, 8))
            plt.plot(year_months, rolling_sums, label='Retail and Food Services Rolling Sum')
            plt.plot(year_months, rolling_averages, label='Retail and Food Services Rolling Average', linestyle='--')

            plt.xlabel('Year')
            plt.ylabel('Values')
            plt.title('Q3D1 - Rolling Sum and Average for Retail and Food Services')
            plt.legend()

            # Set xticks to only the unique years, positioning them at the start of each year (assuming January data is present)
            plt.xticks([f"{year}-01" for year in unique_years], unique_years)

            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        # Q3D2: Modified SQL Query for Retail and Food Services group only
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
            SELECT NC.NAIC_Code_ID
            FROM NAIC_Groups NG
            JOIN NAIC_Group_Mapping NGM ON NG.Group_ID = NGM.Group_ID
            JOIN NAIC_Codes NC ON NGM.NAIC_Code = NC.NAIC_Code
            WHERE NG.Group_Name = 'Retail and Food Services'
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
        plt.title('Q3D2 - Monthly Total Sales for Retail and Food Services Group')

        # Customizing the plot
        plt.legend()

        # Set xticks to only the unique years, positioning them at the start of each year
        # Assuming the data contains January for all the years which you would want to use as the tick mark
        plt.xticks([f"{year}-01" for year in unique_years], unique_years)

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show the plot
        plt.show()

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
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    main()
