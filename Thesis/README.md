# DEPOSITIONAL ENVIRONMENTS OF TEXAS CRETACEOUS CARBONATE PLATFORMS INFERRED FROM THE STATISTICAL ANALYSIS OF GEOCHEMICAL DATA

## Overview
This thesis project is focused on the analysis of geochemical abundances in different geological formations across various locations in Texas. Conducted by Ken Walsh from The University of Texas at San Antonio, the project utilizes statistical and clustering techniques to uncover patterns and relationships within the geochemical data, contributing to a broader understanding of geological characteristics in the region.

## Files Description
The project folder contains two primary files:

- **Thesis.R**: This R script file encompasses the entire data analysis workflow, including data loading, preprocessing, standardization of datasets, calculation of Euclidean distances for cluster analysis, and various visualizations to represent the findings.
- **reCombined.xlsx**: This Excel file contains the raw geochemical abundance data collected from different geological formations across multiple locations. The data includes both qualitative and quantitative variables, serving as the foundation for the analysis performed in the `Thesis.R` script.

## Getting Started

### Prerequisites
Ensure you have R and RStudio installed on your system to run the R script. Additionally, the script requires several R packages, which can be installed using the following commands:

```R
install.packages("devtools")
devtools::install_github("kassambara/factoextra")
install.packages("corrplot")
devtools::install_github("tidyverse/ggplot2")
install.packages("Hmisc")
devtools::install_github("kassambara/ggpubr")
devtools::install_github("yihui/knitr")
```
## Running the Analysis
1. Clone this repository to your local machine.
2. Open the `Thesis.R` script in RStudio.
3. Set the working directory to the location of the cloned repository.
4. Run the `Thesis.R` script to perform the analysis.

## Data Analysis Workflow
The analysis workflow includes the following key steps:

- **Data Loading**: Importing the geochemical data from the `reCombined.xlsx` file.
- **Data Preprocessing**: Creating subsets based on geological formations and locations, handling missing data.
- **Data Standardization**: Standardizing the quantitative variables to have a mean of 0 and a standard deviation of 1.
- **Cluster Analysis**: Calculating Euclidean distances and performing hierarchical clustering to identify patterns in the data.
- **Visualization**: Generating various plots, including correlation matrices, PCA plots, and dendrograms to visualize the clustering results.

## Contributions
This project is part of the thesis work conducted by Ken Walsh. Contributions, suggestions, and questions are welcome.

## License
This project is licensed under the typical academic license for theses at The University of Texas at San Antonio. See the university's thesis publication guidelines for more details.

## Contact
For any queries or further discussion, feel free to [contact me](https://kenwalsh16.github.io/#contact).
