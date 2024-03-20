## Installing required R Packages List of pacakges requiring install if you do not already have them. Dependencies will be install as well.

# install_github("kassambara/factoextra", dependencies = TRUE)
# install.packages('devtools', dependencies = TRUE)
# install.packages("corrplot", dependencies = TRUE)
# install_github("gridExtra", dependencies = TRUE)
# install_github("ggplot2", dependencies = TRUE)
# install.packages("Hmisc", dependencies = TRUE)
# install_github("ggpubr", dependencies = TRUE)
# install_github("knitr", dependencies = TRUE)


## Requiring libraries to be loaded before R code is R

require(factoextra)
require(gridExtra)
require(devtools)
require(corrplot)
require(ggplot2)
require(ggpubr)
require(knitr)
require(Hmisc)

# Function called later in the code if you use the rcorr functionality. flattenCorrMatrix cormat : matrix of the correlation coefficients. pmat : matrix of the correlation p-values.
flattenCorrMatrix <- function(cormat, pmat) {
  ut <- upper.tri(cormat)
  data.frame(
    row = rownames(cormat)[row(cormat)[ut]],
    column = rownames(cormat)[col(cormat)[ut]],
    cor  =(cormat)[ut],
    p = pmat[ut]
  )
}

## Preparing Data Sets the location of the directory you wish to use for the ptoject. Note: inside the "" you use / instead of  to separate diirectories Windows OS standard is to use  to ## separate directories. Commented Out because Working Directory is set.

# setwd("/Users/w_fh0/Google Drive/College/Thesis/Data/Thesis/Data")

## Loading the Data First line imports the complete dataset from a tab delimited text file ### created in Excel row.names = NULL tells R that it is not to name the rows. Optional command ## header = TRUE would tell R that the first row is the name of the columns.

combined <- read.csv(file='reCombined.txt', sep = '\t', row.names = NULL)

## Examining the Data Frame combined. The combined dataset has 296 rows by 23 columns. The first four columns are qualitative variables (Location, Sample, Strat Position, and Group).
## Columns 5 through 23 are the geochemical abundances
## Combined's data structure

str(combined)

## First 6 entries of the Combined dataset

head(combined)

## Creating the subsets from Combined. Location 1 is in Southwest Texas, Location 2 is Central Texas AC indicates Austin Chalk Formation, GR = Glen Rose, 1a & 1b from Big Bend. AC2 dataset ## has no data for the following elements, U, Th, Cr, and Ni. We remove those columns from the dataset so we do not introduce NaNs. This step must be done for any #datasets that have no 
## data for an element. When compiling the Excel data note what mineral data is missing for what location. From this dataset you can count the column numbers that correspond to the 
## elements that need to be removed.

ac1 <- as.data.frame(subset(combined, Location == "AC.ST"))
ac2 <- as.data.frame(subset(combined[, -c(7:8, 22:23)], Location == "AC.CT"))
ac12 <- as.data.frame(subset(combined, Location == "AC.ST" | Location == "AC.CT"))
gr1 <- as.data.frame(subset(combined, Location == "GR.ST"))
gr2 <- as.data.frame(subset(combined[, -c(8, 10)], Location == "GR.CT"))
gr12 <- as.data.frame(subset(combined, Location == "GR.ST" | Location == "GR.CT"))
acgr1 <- as.data.frame(subset(combined, Location == "AC.ST" | Location == "GR.ST"))
acgr2 <- as.data.frame(subset(combined[, -c(7:8, 22:23)], 
                              Location == "AC.CT" | Location == "GR.CT"))

##Displaying the Structure of the Dataset and the first six lines of the dataset.

str(combined)
head(combined)

## Standardizing all of the Datasets. Standardizing the only the quantative data in the datasets for my datasets, columns 1-4 contained qualitative data, that cannot be standardized. 
## Therefore I pass to the scale function only my quantitative data, this will vary for my dataset because columns needed to be removed to create the subsets. Standardizing so Mean = 0 and ## StDev = 1, centering the data on the origin

combined.sc <- scale(combined[, (5:23)], center = TRUE, scale = TRUE)
ac1.sc <- scale(ac1[, (5:23)], center = TRUE, scale = TRUE)
ac2.sc <- scale(ac2[, (5:19)], center = TRUE, scale = TRUE)
ac12.sc <- scale(ac12[, (5:23)], center = TRUE, scale = TRUE)
gr1.sc <- scale(gr1[, (5:23)], center = TRUE, scale = TRUE)
gr2.sc <- scale(gr2[, (5:19)], center = TRUE, scale = TRUE)
gr12.sc <- scale(gr12[, (5:23)], center = TRUE, scale = TRUE)
acgr1.sc <- scale(acgr1[, (5:23)], center = TRUE, scale = TRUE)
acgr2.sc <- scale(acgr2[, (5:19)], center = TRUE, scale = TRUE)

##Determining the Eucleadian Distance for use in Cluster Analysis. Q-Mode - Pass only quantative variables and the tranpose of the matrix to dist().

distQ.combined <- as.table(dist(t(combined.sc)), method = "euclidean")
distQ.ac1 <- as.table(dist(t(ac1.sc)), method = "euclidean")
distQ.ac2 <- as.table(dist(t(ac2.sc)), method = "euclidean")
distQ.ac12 <- as.table(dist(t(ac12.sc)), method = "euclidean")
distQ.gr1 <- as.table(dist(t(gr1.sc)), method = "euclidean")
distQ.gr2 <- as.table(dist(t(gr2.sc)), method = "euclidean")
distQ.gr12 <- as.table(dist(t(gr12.sc)), method = "euclidean")
distQ.acgr1 <- as.table(dist(t(acgr1.sc)), method = "euclidean")
distQ.acgr2 <- as.table(dist(t(acgr2.sc)), method = "euclidean")

## Print Single Example of Euclidean Matrix

print(distQ.combined)

## R-Mode - Pass only quantative variables to dist(). No transpose of matrix.

distR.combined <- as.table(dist(combined.sc), method = "euclidean")
distR.ac1 <- as.table(dist(ac1.sc), method = "euclidean")
distR.ac2 <- as.table(dist(ac2.sc), method = "euclidean")
distR.ac12 <- as.table(dist(ac12.sc), method = "euclidean")
distR.gr1 <- as.table(dist(gr1.sc), method = "euclidean")
distR.gr2 <- as.table(dist(gr2.sc), method = "euclidean")
distR.gr12 <- as.table(dist(gr12.sc), method = "euclidean")
distR.acgr1 <- as.table(dist(acgr1.sc), method = "euclidean")
distR.acgr2 <- as.table(dist(acgr2.sc), method = "euclidean")

## To use Ward’s method in hclust(), the distance must be squared. Q-Mode

distQ.combined <- distQ.combined^2
distQ.ac1 <- distQ.ac1^2
distQ.ac2 <- distQ.ac2^2
distQ.ac12 <- distQ.ac12^2
distQ.gr1 <- distQ.gr1^2
distQ.gr2 <- distQ.gr2^2
distQ.gr12 <- distQ.gr12^2
distQ.acgr1 <- distQ.acgr1^2
distQ.acgr2 <- distQ.acgr2^2

## R-Mode

distR.combined <- distR.combined^2
distR.ac1 <- distR.ac1^2
distR.ac2 <- distR.ac2^2
distR.ac12 <- distR.ac12^2
distR.gr1 <- distR.gr1^2
distR.gr2 <- distR.gr2^2
distR.gr12 <- distR.gr12^2
distR.acgr1 <- distR.acgr1^2
distR.acgr2 <- distR.acgr2^2

## Creates Correlation Matrices for all datasets and puts data into a variable for later use.

cor.comb.mat <- as.table(round(cor(combined[, 5:23]),2), method = "pearson")
cor.ac1.mat <- as.table(round(cor(ac1[, 5:23]),2), method = "pearson")
cor.ac2.mat <- as.table(round(cor(ac2[, 5:19]),2), method = "pearson")
cor.ac12.mat <- as.table(round(cor(ac12[, 5:23]),2), method = "pearson")
cor.gr1.mat <- as.table(round(cor(gr1[, 5:23]),2), method = "pearson")
cor.gr2.mat <- as.table(round(cor(gr2[, 5:17]),2), method = "pearson")
cor.gr12.mat <- as.table(round(cor(gr12[, 5:23]),2), method = "pearson")
cor.acgr1.mat <- as.table(round(cor(acgr1[, 5:23]),2), method = "pearson")
cor.acgr2.mat <- as.table(round(cor(acgr2[, 5:19]),2), method = "pearson")

##Displaying Correlation Matrices

print(cor.comb.mat)
print(cor.ac1.mat)
print(cor.ac2.mat)
print(cor.ac12.mat)
print(cor.gr1.mat)
print(cor.gr2.mat)
print(cor.gr12.mat)
print(cor.acgr1.mat)
print(cor.acgr2.mat)

## rcorr Computes a matrix of Pearson’s r or Spearman’s rho rank correlation. Coefficients for all possible pairs of columns of a matrix.

rcomb <- rcorr(cor.comb.mat, type = "pearson")
rac1 <-rcorr(cor.ac1.mat, type = "pearson")
rac2 <-rcorr(cor.ac2.mat, type = "pearson")
rac12 <- rcorr(cor.ac12.mat, type = "pearson")
rgr1 <- rcorr(cor.gr1.mat, type = "pearson")
rgr2 <- rcorr(cor.gr2.mat, type = "pearson")
rgr12 <- rcorr(cor.gr12.mat, type = "pearson")
racgr1 <- rcorr(cor.acgr1.mat, type = "pearson")
racgr2 <- rcorr(cor.acgr2.mat, type = "pearson")

## Printing rcorr matrix

print(rcomb)
print(rac1)
print(rac2)
print(rac12)
print(rgr1)
print(rgr2)
print(rgr12)
print(racgr1)
print(racgr2)

## Summary Statistics for Each Dataset

combstats <- as.table(summary(combined[, 1, 5:23]))
ac1stats <- as.table(summary(ac1))
ac2stats <- as.table(summary(ac2))
ac12stats <- as.table(summary(ac12))
gr1stats <- as.table(summary(gr1))
gr2stats <- as.table(summary(gr2))
gr12stats <- as.table(summary(gr12))
acgr1stats <- as.table(summary(acgr1))
acgr2stats <- as.table(summary(acgr2))

## Printing Summary Stats
print(combstats)
print(ac1stats)
print(ac2stats)
print(ac12stats)
print(gr1stats)
print(gr2stats)
print(gr12stats)
print(acgr1stats)
print(acgr2stats)

##Performing PCA using prcomp().

pca.comb <- prcomp(combined.sc, scale. = TRUE, center = TRUE)
pca.ac1 <- prcomp(ac1.sc, scale. = TRUE, center = TRUE)
pca.ac2 <- prcomp(ac2.sc, scale. = TRUE, center = TRUE)
pca.ac12 <- prcomp(ac12.sc, scale. = TRUE, center = TRUE)
pca.gr1 <- prcomp(gr1.sc, scale. = TRUE, center = TRUE)
pca.gr2 <- prcomp(gr2.sc, scale. = TRUE, center = TRUE)
pca.gr12 <- prcomp(gr12.sc, scale. = TRUE, center = TRUE)
pca.acgr1 <- prcomp(acgr1.sc, scale. = TRUE, center = TRUE)
pca.acgr2 <- prcomp(acgr2.sc, scale. = TRUE, center = TRUE)

##Calculating Std Deviation, Variance Proportions and Cumulative Proportions.

sum.comb <- summary(pca.comb)
sum.ac1 <- summary(pca.ac1)
sum.ac2 <- summary(pca.ac2)
sum.ac12 <- summary(pca.ac12)
sum.gr1 <- summary(pca.gr1)
sum.gr2 <- summary(pca.gr2)
sum.gr12 <- summary(pca.gr12)
sum.acgr1 <- summary(pca.acgr1)
sum.acgr2 <- summary(pca.acgr2)

## Printing Std Deviation, Variance Proportions and Cumulative Proportions.

print(sum.comb)
print(sum.ac1)
print(sum.ac2)
print(sum.ac12)
print(sum.gr1)
print(sum.gr2)
print(sum.gr12)
print(sum.acgr1)
print(sum.acgr2)

##—> Giving user-friendly names to the matrices generated by prcomp() Printing Example Tables for Each Category on the Combined Dataset.

var.comb <- (pca.comb$sdev)^2
var.ac1 <- (pca.ac1$sdev)^2
var.ac2 <- (pca.ac2$sdev)^2
var.ac12 <- (pca.ac12$sdev)^2
var.gr1 <- (pca.gr1$sdev)^2
var.gr2 <- (pca.gr2$sdev)^2
var.gr12 <- (pca.gr12$sdev)^2
var.acgr1 <- (pca.acgr1$sdev)^2
var.acgr2 <- (pca.acgr2$sdev)^2

print(var.comb)

load.comb <- pca.comb$rotation
load.ac1 <- pca.ac1$rotation
load.ac2 <- pca.ac2$rotation
load.ac12 <- pca.ac12$rotation
load.gr1 <- pca.gr1$rotation
load.gr2 <- pca.gr2$rotation
load.gr12 <- pca.gr12$rotation
load.acgr1 <- pca.acgr1$rotation
load.acgr2 <- pca.acgr2$rotation

print(load.comb)

rownames(load.comb) <- colnames(combined.sc)
rownames(load.ac1) <- colnames(ac1.sc)
rownames(load.ac2) <- colnames(ac2.sc)
rownames(load.ac12) <- colnames(ac12.sc)
rownames(load.gr1) <- colnames(gr1.sc)
rownames(load.gr2) <- colnames(gr2.sc)
rownames(load.gr12) <- colnames(gr12.sc)
rownames(load.acgr1) <- colnames(acgr1.sc)
rownames(load.acgr2) <- colnames(acgr2.sc)

scores.comb <- pca.comb$x
scores.ac1 <- pca.ac1$x
scores.ac2 <- pca.ac2$x
scores.ac12 <- pca.ac12$x
scores.gr1 <- pca.gr1$x
scores.gr2 <- pca.gr2$x
scores.gr12 <- pca.gr12$x
scores.acgr1 <- pca.acgr1$x
scores.acgr2 <- pca.acgr2$x

print(scores.comb)

var.comb <- var.comb/sum(var.comb) * 100
var.ac1 <- var.ac1/sum(var.ac1) * 100
var.ac2 <- var.ac2/sum(var.ac2) * 100
var.ac12 <- var.ac12/sum(var.ac12) * 100
var.gr1 <- var.gr1/sum(var.gr1) * 100
var.gr2 <- var.gr2/sum(var.gr2) * 100
var.gr12 <- var.gr12/sum(var.gr12) * 100
var.acgr1 <- var.acgr1/sum(var.acgr1) * 100
var.acgr2 <- var.acgr2/sum(var.acgr2) * 100

print(var.comb)

## Creates barplots showing PCs contribution to variances, # and the number of PCs that are considered ##relevant to the analysis for each dataset.

barplot(var.comb, xlab='PC', ylab='Combined Dataset % Variance',
        names.arg=1:length(var.comb), las=1, col='gray')
abline(h=1/ncol(combined)*100, col="red")
 
barplot(var.ac1, xlab='PC', ylab='AC ST Percent Variance',
        names.arg=1:length(var.ac1), las=1, col='gray')
abline(h=1/ncol(ac1)*100, col="red")
 
barplot(var.ac2, xlab='PC', ylab='AC CT Percent Variance',
        names.arg=1:length(var.ac2), las=1, col='gray')
abline(h=1/ncol(acgr2)*100, col="red")
 
barplot(var.ac12, xlab='PC', ylab='ST & CT AC Percent Variance',
        names.arg=1:length(var.ac12), las=1, col='gray')
abline(h=1/ncol(ac12)*100, col="red")
 
barplot(var.gr1, xlab='PC', ylab='GR ST Percent Variance',
        names.arg=1:length(var.gr1), las=1, col='gray')
abline(h=1/ncol(gr1)*100, col="red")
 
barplot(var.gr2, xlab='PC', ylab='GR CT Percent Variance',
        names.arg=1:length(var.gr2), las=1, col='gray')
abline(h=1/ncol(gr2)*100, col="red")
 
barplot(var.gr12, xlab='PC', ylab='ST & CT GR Percent Variance',
        names.arg=1:length(var.gr12), las=1, col='gray')
abline(h=1/ncol(gr12)*100, col="red")
 
barplot(var.acgr1, xlab='PC', ylab='ST AC & GR Percent Variance',
        names.arg=1:length(var.acgr1), las=1, col='gray')
abline(h=1/ncol(acgr1)*100, col="red")
 
barplot(var.acgr2, xlab='PC', ylab='CT AC & GR Percent Variance',
        names.arg=1:length(var.acgr2), las=1, col='gray')
abline(h=1/ncol(acgr2)*100, col="red")
 
## Creating variable weightings table from the PCA, and rounding them to two decimal places.

combl <- round(load.comb, 2)[ , 1:7]
ac1l <- round(load.ac1, 2)[ , 1:4]
ac2l <- round(load.ac2, 2)[ , 1:5]
ac12l <- round(load.ac12, 2)[ , 1:4]
gr1l <- round(load.gr1, 2)[ , 1:6]
gr2l <- round(load.gr2, 2)[ , 1:7]
gr12l <- round(load.gr12, 2)[ , 1:7]
acgr1l <- round(load.acgr1, 2)[ , 1:6]
acgr2l <- round(load.acgr2, 2)[ , 1:5]

## Printing the Tables

print(combl)
print(ac2l)
print(ac12l)
print(gr1l)
print(gr2l)
print(gr12l)
print(acgr1l)
print(acgr2l)

## Correlation Plots where Insignificant correlations are left blank.

corrplot(rcomb$r, type="upper", order="hclust", 
         p.mat = rcomb$P, sig.level = 0.01, insig = "blank")
 
corrplot(rac1$r, type="upper", order="hclust", 
         p.mat = rac1$P, sig.level = 0.01, insig = "blank")
 
corrplot(rac2$r, type="upper", order="hclust", 
         p.mat = rac2$P, sig.level = 0.01, insig = "blank")
 
corrplot(rac12$r, type="upper", order="hclust", 
         p.mat = rac12$P, sig.level = 0.01, insig = "blank")
 
corrplot(rgr1$r, type="upper", order="hclust", 
         p.mat = rgr1$P, sig.level = 0.01, insig = "blank")
 
corrplot(rgr2$r, type="upper", order="hclust", 
         p.mat = rgr2$P, sig.level = 0.01, insig = "blank")
 
corrplot(rgr12$r, type="upper", order="hclust", 
         p.mat = rgr12$P, sig.level = 0.01, insig = "blank")
 
corrplot(racgr1$r, type="upper", order="hclust", 
         p.mat = racgr1$P, sig.level = 0.01, insig = "blank")
 
corrplot(racgr2$r, type="upper", order="hclust", 
         p.mat = racgr2$P, sig.level = 0.01, insig = "blank")
 
## PCA Variance Plots displaying top 10 PCs per %Variance

fviz_eig(pca.comb, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "Combined Dataset PCs & Variance", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.ac1, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "AC ST PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.ac2, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "AC CT PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.ac12, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "ST & CT Austin Chalk PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.gr1, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "GR ST PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.gr2, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "GR CT PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.gr12, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "ST & CT Glen Rose PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.acgr1, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "South Texas PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
fviz_eig(pca.acgr2, choice = c("variance", "eigenvalue"), 
         geom = c("bar","line"), barfill = "steelblue", barcolor = "steelblue", 
         linecolor = "black", ncp = 10, addlabels = TRUE, hjust = 0, 
         main = "Central Texas PCs & Variances", 
         xlab = NULL, ylab = NULL, ggtheme = theme_minimal(), ylim = c(0, 50))
 
## Calculating Eigenvalue Matrices

combeig <- as.matrix(get_eig(pca.comb))
ac1eig <- as.matrix(get_eig(pca.ac1))
ac2eig <- as.matrix(get_eig(pca.ac2))
ac12eig <- as.matrix(get_eig(pca.ac12))
gr1eig <- as.matrix(get_eig(pca.gr1))
gr2eig <- as.matrix(get_eig(pca.gr2))
gr12eig <- as.matrix(get_eig(pca.gr12))
acgr1eig <- as.matrix(get_eig(pca.acgr1))
acgr2eig <- as.matrix(get_eig(pca.acgr2))

## Printing Eigenvalue Matrices

print(combeig)
print(ac1eig)
print(ac2eig)
print(ac12eig)
print(gr1eig)
print(gr2eig)
print(gr12eig)
print(acgr1eig)
print(acgr2eig)

## Top 10 Variable Contribution Plots, control variable colors using their contributions To get all of the variables to plot on the circle, the line “select.var = list(contrib = 10)” must ## be removed.

fviz_pca_var(pca.comb, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE, 
             title = "Combined Dataset Variables PCA",
             select.var = list(contrib = 10))
 
fviz_pca_var(pca.ac1, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "AC ST Dataset Variables PCA")
 
fviz_pca_var(pca.ac2, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "AC CT Dataset Variables PCA")
 
fviz_pca_var(pca.ac12, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "ST & CT AC Dataset Variables PCA")
 
fviz_pca_var(pca.gr1, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "GR ST Dataset Variables PCA")
 
fviz_pca_var(pca.gr2, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "GR CT Dataset Variables PCA")
 
fviz_pca_var(pca.gr12, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "ST & CT GR Dataset Variables PCA")
 
fviz_pca_var(pca.acgr1, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "ST AC & GR Dataset Variables PCA")
 
fviz_pca_var(pca.acgr2, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE, # Avoid text overlapping 
             autolab = TRUE,
             title = "CT AC & GR Dataset Variables PCA")
 
## Histograms displaying Top 10 Variable Contributions to PC1 and PC2 separately

fviz_contrib(pca.comb, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to Combined's PC1")
 
fviz_contrib(pca.comb, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to Combined's PC2")
 
fviz_contrib(pca.ac1, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to AC ST Dataset's PC1")
 
fviz_contrib(pca.ac1, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to AC ST Dataset's PC2")
 
fviz_contrib(pca.ac2, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to AC CT Dataset's PC1")
 
fviz_contrib(pca.ac2, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to AC CT Dataset's PC2")
 
fviz_contrib(pca.ac12, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to ST & CT AC PC1")
 
fviz_contrib(pca.ac12, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to ST & CT AC PC2")
 
fviz_contrib(pca.gr1, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to GR ST PC1")
 
fviz_contrib(pca.gr1, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to GR ST PC2")
 
fviz_contrib(pca.gr2, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to GR CT PC1")
 
fviz_contrib(pca.gr2, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to GR CT PC2")
 
fviz_contrib(pca.gr12, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to ST & CT GR PC1")
 
fviz_contrib(pca.gr12, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to ST & CT GR PC2")
 
fviz_contrib(pca.acgr1, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to ST AC & GR PC1")
 
fviz_contrib(pca.acgr1, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to ST AC & GR PC2")
 
fviz_contrib(pca.acgr2, choice = "var", axes = 1, top = 10, 
             title = "Variable Contribution to CT AC & GR PC1")
 
fviz_contrib(pca.acgr2, choice = "var", axes = 2, top = 10, 
             title = "Variable Contribution to CT AC & GR PC2")
 
## Top 10 Biplot of individuals and variables Keep only the labels for variables.

fviz_pca_biplot(pca.comb, label = "var", palette = "lancet", 
                habillage = combined$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "Combined Dataset Variables & Individuals",
                select.var = list(contrib = 10))
 
fviz_pca_biplot(pca.ac1, label = "var", 
                habillage = ac1$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "AC ST Dataset Variables & Individuals", 
                select.var = list(contrib = 10))
 
fviz_pca_biplot(pca.ac2, label = "var", 
                habillage = ac2$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "AC CT Dataset Top 10 Variables", 
                select.var = list(contrib = 10))
 
fviz_pca_biplot(pca.ac12, label = "var", 
                habillage = ac12$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "ST & CT AC Dataset Top 10 Variables", 
                select.var = list(contrib = 10))
 
fviz_pca_biplot(pca.gr1, label = "var", 
                habillage = gr1$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "GR ST Dataset Top 10 Variables", 
                select.var = list(contrib = 10))
 
fviz_pca_biplot(pca.gr2, label = "var", 
                habillage = gr2$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "GR CT Dataset Top 10 Variables", 
                select.var = list(contrib = 10))
 
fviz_pca_biplot(pca.gr12, label = "var", 
                habillage = gr12$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "ST & CT GR Dataset Top 10 Variables", 
                )
 
fviz_pca_biplot(pca.acgr1, label = "var", 
                habillage = acgr1$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "ST AC & GR Dataset Top 10 Variables", 
                select.var = list(contrib = 10))
 
fviz_pca_biplot(pca.acgr2, label = "var", 
                habillage = acgr2$Location,
                repel = TRUE, ggtheme = theme_minimal(), 
                title = "CT AC & GR Dataset Top 10 Variables", 
                select.var = list(contrib = 10))
 
## Pulling data for the Individuals Plotting

res.comb <- get_pca_ind(pca.comb)
res.ac1 <- get_pca_ind(pca.ac1)
res.ac2 <- get_pca_ind(pca.ac2)
res.ac12 <- get_pca_ind(pca.ac12)
res.gr1 <- get_pca_ind(pca.gr1)
res.gr2 <- get_pca_ind(pca.gr2)
res.gr12 <- get_pca_ind(pca.gr12)
res.acgr1 <- get_pca_ind(pca.acgr1)
res.acgr2 <- get_pca_ind(pca.acgr2)

## Adding the coordinate data from the first 5 PCs to the dataset for plotting purposes.

acombine <- cbind(combined, res.comb$coord[, 1:5])
aac1 <- cbind(ac1, res.ac1$coord[, 1:5])
aac2 <- cbind(ac2, res.ac2$coord[, 1:5])
aac12 <- cbind(ac12, res.ac12$coord[, 1:5])
agr1 <- cbind(gr1, res.gr1$coord[, 1:5])
agr2 <- cbind(gr2, res.gr2$coord[, 1:5])
agr12 <- cbind(gr12, res.gr12$coord[, 1:5])
aacgr1 <- cbind(acgr1, res.acgr1$coord[, 1:5])
aacgr2 <- cbind(acgr2, res.acgr2$coord[, 1:5])

## Plotting 95% CI Ellipses around data points grouped by Location

comb <- ggplot(acombine, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

combplot <- comb + ggtitle("95% C.I. for Combined Datasets") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(combplot)

ac1p <- ggplot(aac1, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

ac1plot <- ac1p + ggtitle("95% C.I. for AC ST") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(ac1plot)
 
ac2p <- ggplot(aac2, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

ac2plot <- ac2p + ggtitle("95% C.I. for AC CT") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(ac2plot)
 
ac12p <- ggplot(aac12, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

ac12plot <- ac12p + ggtitle("95% C.I. for Austin Chalk Datasets") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(ac12plot)
 
gr1p <- ggplot(agr1, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

gr1plot <- gr1p + ggtitle("95% C.I. for GR ST") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(gr1plot)
 
gr2p <- ggplot(agr2, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

gr2plot <- gr2p + ggtitle("95% C.I. for GR CT") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(gr2plot)
 
gr12p <- ggplot(agr12, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

gr12plot <- gr12p + ggtitle("95% C.I. for Glen Rose Datasets") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(gr12plot)
 
acgr1p <- ggplot(aacgr1, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

acgr1plot <- acgr1p + ggtitle("95% C.I. for South Texas Datasets") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(acgr1plot)
 
acgr2p <- ggplot(aacgr2, aes(Dim.1, Dim.2, col = Location, fill = Location)) + 
  stat_ellipse(geom = 'polygon', col = 'black', alpha = 0.5) + 
  geom_point(shape = 21, col = 'black')

acgr2plot <- acgr2p + ggtitle("95% C.I. for Central Texas Datasets") + 
  scale_x_continuous(name = "PC1", limits = c(-5, 5)) +
  scale_y_continuous(name = "PC2", limits = c(-5, 5))

print(acgr2plot)
 
## Heat Maps for the Euclidean Distances Red = High Similarity (low dissimilarity); blue = Low Similarity

fviz_dist(distQ.combined)
 
fviz_dist(distQ.ac1)
 
fviz_dist(distQ.ac2)
 
fviz_dist(distQ.ac12)
 
fviz_dist(distQ.gr1)
 
fviz_dist(distQ.gr2)
 
fviz_dist(distQ.gr12)
 
fviz_dist(distQ.acgr1)
 
fviz_dist(distQ.acgr2)
 
## Hierarchical Clustering Analysis - Dendrograms using Ward No.2 Method Q-mode

hcWD.comb <- hclust(distQ.combined, method = "ward.D2")
plot(hcWD.comb, main = "Combined Dataset Clustering")
rect.hclust(hcWD.comb, k = 5, border = 'red')
 
clusterWQc <- cutree(hcWD.comb, 5)

hcWD.ac1 <- hclust(distQ.ac1, method = "ward.D2")
plot(hcWD.ac1, main = "AC ST Clustering")
rect.hclust(hcWD.ac1, k = 3, border = 'red')
 
clusterWQac1 <- cutree(hcWD.ac1, 3)

hcWD.ac2 <- hclust(distQ.ac2, method = "ward.D2")
plot(hcWD.ac2, main = "AC CT Clustering")
rect.hclust(hcWD.ac2, k = 3, border = 'red')
 
clusterWQac2 <- cutree(hcWD.ac2, 3)

hcWD.ac12 <- hclust(distQ.ac12, method = "ward.D2")
plot(hcWD.ac12, main = "ST & CT Austin Chalk Clustering")
rect.hclust(hcWD.ac12, k = 3, border = 'red')
 
clusterWQac12 <- cutree(hcWD.ac12, 3)

hcWD.gr1 <- hclust(distQ.gr1, method = "ward.D2")
plot(hcWD.gr1, main = "GR ST Clustering")
rect.hclust(hcWD.gr1, k = 5, border = 'red')
 
clusterWQgr1 <- cutree(hcWD.gr1, 5)

hcWD.gr2 <- hclust(distQ.gr2, method = "ward.D2")
plot(hcWD.gr2, main = "GR CT Clustering")
rect.hclust(hcWD.gr2, k = 4, border = 'red')
 
clusterWQgr2 <- cutree(hcWD.gr2, 4)

hcWD.gr12 <- hclust(distQ.gr12, method = "ward.D2")
plot(hcWD.gr12, main = "ST & CT Glen Rose Clustering")
rect.hclust(hcWD.gr12, k = 4, border = 'red')
 
clusterWQgr12 <- cutree(hcWD.gr12, 4)

hcWD.acgr1 <- hclust(distQ.acgr1, method = "ward.D2")
plot(hcWD.acgr1, main = "South Texas AC & GR Clustering")
rect.hclust(hcWD.acgr1, k = 6, border = 'red')
 
clusterWQacgr1 <- cutree(hcWD.acgr1, 6)

hcWD.acgr2 <- hclust(distQ.acgr2, method = "ward.D2")
plot(hcWD.acgr2, main = "Central Texas AC & GR Clustering")
rect.hclust(hcWD.acgr2, k = 2, border = 'red')
 
clusterWQacgr2 <- cutree(hcWD.acgr2, 2)
##End of Script
