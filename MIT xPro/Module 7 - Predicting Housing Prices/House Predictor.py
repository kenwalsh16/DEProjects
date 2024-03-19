# Project - Build a house price predictive model
# y (House Price) = x1 (Column from Data)m1 (Must be determined) + ... + xnmn + b

# Import necessary libraries
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Read the data from CSV file
data = pd.read_csv('houseSmallData.csv')
print('Shape of the Data Matrix:', data.shape)
print('Sample of the Data:', data.head())

# Select a subset of data for training
train = data.iloc[0:20, :]

# Graphs
# Select the variables of interest
# Chosen Variables
variables_of_interest = ['OverallQual', 'MasVnrArea', 'FullBath', 'YearBuilt', 'GarageArea', 'GrLivArea', 'GarageCars', 'LotArea']

# Rejected Variables
#variables_of_interest = ['WoodDeckSF', 'MoSold', 'TotalBsmtSF', 'BsmtFinSF1', '1stFlrSF', '2ndFlrSF', 'GarageYrBlt', 'LotFrontage', 'TotRmsAbvGrd', 'BedroomAbvGr', 'Fireplaces', 'YearRemodAdd']

# Create scatter plots
# Calculate the number of rows and columns for the subplot grid
num_rows = 3
num_cols = 4

# Create the subplot grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(16, 12))

# Flatten the axes array to iterate over it easily
axes = axes.flatten()

# Create scatter plots for each variable
for i, variable in enumerate(variables_of_interest):
    ax = axes[i]
    sns.scatterplot(x=data[variable], y=data['SalePrice'], ax=ax)
    ax.set_xlabel(variable)
    ax.set_ylabel('Sale Price')
    ax.set_title(f'{variable} vs. Sale Price')

# Remove any empty subplots if the number of variables is less than 12
if len(variables_of_interest) < num_rows * num_cols:
    for j in range(len(variables_of_interest), num_rows * num_cols):
        fig.delaxes(axes[j])

# Adjust the spacing between subplots
plt.tight_layout()

# Prepare the data for regression
# Select all of the columns with numerical data and assign them to numeric for correlation
numeric = train.select_dtypes(include=[np.number])
train = train.fillna(0)
data = data.fillna(0)

# Compute the correlation matrix
# Run the correlation function on the numerical columns and assign the highest twenty columns correlated to "SalePrice" to a new variable called bestCols
corr = numeric.corr()
bestCols = corr['SalePrice'].sort_values(ascending=False)[0:21].index

# Create the the X variables featuring the best twenty numerical columns correlated to "SalePrice"
trainX = train[bestCols]
fullX = data[bestCols]

# Creating our X and Y for our linear regression model for our training data - drop any columns considered not necessary from trainX
trainY = train['SalePrice']
trainX = trainX.drop(['SalePrice', 'WoodDeckSF', 'MoSold', 'TotalBsmtSF', 'BsmtFinSF1', '1stFlrSF', '2ndFlrSF', 'GarageYrBlt', 'LotFrontage', 'TotRmsAbvGrd', 'BedroomAbvGr', 'Fireplaces', 'YearRemodAdd'], axis = 1)

# Creating our X and Y for our linear regression model for our full dataset - drop any columns considered not necessary from fullX
fullY = data['SalePrice']
fullX = fullX.drop(['SalePrice', 'WoodDeckSF', 'MoSold', 'TotalBsmtSF', 'BsmtFinSF1', '1stFlrSF', '2ndFlrSF', 'GarageYrBlt', 'LotFrontage', 'TotRmsAbvGrd', 'BedroomAbvGr', 'Fireplaces', 'YearRemodAdd'], axis = 1)

# Train the linear regression model on the training data
lr = linear_model.LinearRegression()
model = lr.fit(trainX, trainY)
predictions = model.predict(trainX)

# Train the linear regression model on the full dataset
lr = linear_model.LinearRegression()
model1 = lr.fit(fullX, fullY)
predictions = model1.predict(fullX)

# Evaluate the performance of the models
model.score(trainX, trainY)
model1.score(fullX, fullY)