#!/usr/bin/env python
# coding: utf-8

# # data analysis workshop

# Gamble, T., & Walker, I. (2016). Wearing a Bicycle Helmet Can Increase Risk Taking and Sensation Seeking in Adults. <i>Psychological Science, 27</i>(2).
# 
# original paper: https://doi.org/10.1177/0956797615620784
# 
# original data downloaded from: https://osf.io/eky4s/
# 
# PLEASE NOTE: the dataset you are using today has been altered for the purposes of this exercise. 


# ## variables:
# 
# ID: Participant identification number
# 
# Condition: Which condition the participant was in: 1=helmet, 2=cap
# 
# Age: Age in years
# 
# Sex: Gender of the participant: 1=male, 2=female
# 
# STAI pre: State Trait Anxiety Inventory Y state anxiety total before wearing the eye-tracker
# 
# SSS total: Sensation Seeking Scale score
# 
# BART: Balloon Analogue Risk Task adjusted mean (mean number of pumps on trials where the balloon did not burst); 
# assume that MINIMUM BART score = 100; MAXIMUM = 8500
# 
# STAI during: State Trait Anxiety Inventory Y state anxiety total whilst wearing the eye-tracker
# 
# STAI post: State Trait Anxiety Inventory Y state anxiety total after wearing the eye-tracker
# 
# Cycling frequency: How often does the participant cycle: 1=Never, 2=Rarely, 3=At least once a month, 4=At least once a week, 
# 5=At least two to four times a week, 6=Five times a week or more
# 
# Helmet use likelihood: How often does the participant wear a cycle helmet: 0=don’t cycle, 1=never - 7=always
# 

# ## import modules

import pandas as pd     # pandas package imported with an alias. Used for reading csv file and working with DataFrame
import seaborn as sns   # seaborn package imported with an alias. Used for data visualization based on matplotlib and integrates well with pandas
import matplotlib
import matplotlib.pyplot as plt     # pyplot interface from matplotlib package imported. only .show() method is used
import numpy as np


# ### load data

# read in data file as a data frame
helmets_df = pd.read_csv('helmets_data.csv', delimiter=";")
# function to read csv files as DataFrame objects
# file path of an existing file given. Delimiter is how data is separated in the csv file, it could also be "," fx

# print our data
print(helmets_df)


# ## data cleaning

# ### exploring data

# first, let's get general statistics on all the variables.
# do you notice any potentially problematic issues?
helmets_df.describe()       # .describe() method returns basic descriptive statistics of dataframe. Good for spotting outliers
helmets_df.groupby('Condition').agg({'Condition':['count']})
# .groupby() and .agg() methods are used together. groupby creates groups for conditions (there are 2 groups)
# .agg() counts how many condition values are in each group

# #### removing potential duplicates
# why are duplicate data points a problem?
helmets_df = helmets_df.drop_duplicates()       # .drop_duplicates() methods erases duplicate rows, like row 7 in dataset


# #### screening for missing data
# Do we have any empty cells (missing values) in our data? 
# we see that we have some potentially missing values, is that true?
helmets_df.isnull().any()
# .isnull() shows values missing across the whole dataset, .any() shows if there are any missing in a column

# Is that a problem? How is an empty cell different from 0?
# remove rows with empty values
helmets_df = helmets_df.dropna(axis=0, how='any')
# .dropna() method removes missing values, rows 19 and 56 in this dataset
# axis = 0 means rows (1 would be columns)
# how="any" means that the row is removed if there is at least one empty value
# both parameters are defaults, so there was no need to specify them here


# #### locating and removing "illegal" values

# age: what are "illegal" age values? Do we have any of them present in our data?
# age counts
helmets_df.groupby('Age').agg({'Age':['count']})        # see how many people of each age are in the data
# drop rows where cells meet conditions
helmets_df = helmets_df[(helmets_df.Age>=17) & (helmets_df.Age<=65)]
# dataframe is modified with Series intersection - only rows where the age value is equal or over 17 and equal or under 65
# rows 18 and 84 are removed


# sex: what are the "illegal" sex values? Do we have any of them present in our data?
# sex counts
helmets_df['Sex'].value_counts()        # since the only values "allowed" are 1 and 2, values 3 and 12 are illegal
# drop rows where cells meet conditions
helmets_df = helmets_df[(helmets_df.Sex==1) | (helmets_df.Sex==2)]
# Series union - rows that have sex value of 1 and 2
# 2 rows are removed

# BART scores: what are the "illegal" values?
# drop rows where cells meet conditions
helmets_df = helmets_df[(helmets_df.BART>100) & (helmets_df.BART<8500)]
# Series intersection between legal BART values
# 2 rows are removed

# cycling frequency and helmet use likelihood: what are the "illegal" value pairs?
# find rows that specify conditions and drop them
index_name = helmets_df[(helmets_df.Cycling_Frequency==1) & (helmets_df.Helmet_Use_Likelihood!=0)].index
# index means row in DataFrame, so this is identifying which rows have illegal value pairs
helmets_df.drop(index_name, inplace=True)
# .drop() method removes specified rows or columns - row 73
# drops rows where the person does not cycle, but wears a helmet, because they dont make sense logically
# inplace parameter is False by default, but then it does not do the operation

print(helmets_df)

# save our cleaned data file!
helmets_df.to_csv('outFile.csv')
# .to_csv() method writes the DataFrame to csv file, default delimiter is ","


# ## data plotting

# ### scatterplots
sns.scatterplot(data=helmets_df, x='BART', y='SSS_total', hue='Condition', style='Condition')
# a method of the seaborn package the creates a scatterplot
# 2 axis (each have an argument), each with a variable from the dataset (data argument). Important to load the cleaned dataset
# cap and helmet conditions have different color and style (x vs dot), because it is easier to read
plt.show()
# method from the matplotlib package that displays all open plots. Now it is only going to show one
# better to put this method after all the graphs

cap_df = helmets_df[helmets_df.Condition == 1]
hel_df = helmets_df[helmets_df.Condition == 2]
# two DataFrame objects depending on which condition value is in the index (row)

sns.lmplot(x='BART', y='SSS_total', data=cap_df, ci=None).fig.suptitle("condition = cap")
sns.lmplot(x='BART', y='SSS_total', data=hel_df, ci=None).fig.suptitle("condition = helmet")

sns.lmplot(x='BART', y='SSS_total', hue='Condition', data=helmets_df)
# .lmplot() creates regression models for 2 variables from a DataFrame
# ci is confidence interval of the regression model, the more narrow the better
# fig.suptitle is from matplotlib and adds a title to the chart

sns.jointplot(x='BART', y='SSS_total', data=hel_df, kind="reg").fig.suptitle("condition = helmet")
sns.jointplot(x='BART', y='SSS_total', data=cap_df, kind="reg").fig.suptitle("condition = cap")
# .jointplot() creates both univariate and bivariate graphs
# Univariate is a histogram, bivariate is determined with the kind= argument

sns.lmplot(x="BART", y="SSS_total", hue="Condition", col="Sex", data=helmets_df)
# regression models of the complete DataFrame, but the col= splits it in 2 graphs depending on the sex value


# ### histograms
sns.displot(helmets_df, x='BART',bins=15, kde=True)
# displot() draws ditribution plots
# histogram is default, other types of graph can be specified with kind= argument
# bins is the number of blocks on the x axis
# kde adds a kernel density estimator

sns.displot(helmets_df, x='BART', hue='Condition', kde=True)
# hue differentiates condition

sns.displot(helmets_df, x='BART', hue='Condition', multiple='dodge',bins=10, col='Sex', kde=True)
# col= splits graph based on sex value
# multiple= determines if blocks are next to each other or on top (stacked)


# ### kernel density estimation
sns.displot(helmets_df, x='BART', hue='Condition', kind="kde", multiple='stack')
# kind=kde makes it a kernel density estimation graph
# multiple= could be layer or fill, but those dont make sense

# ### boxplot
sns.catplot(data=helmets_df, x="Condition", y="BART", kind="bar")
# .catplot() is a categorical plot function
# kind="bar" makes this a barplot
# black lines are error lines, measures uncertainty of the data

sns.catplot(data=helmets_df, x="Condition", y="BART", kind="box")
# boxplot based on condition
# show distribution and outliers

sns.catplot(data=helmets_df, x="Condition", y="BART", kind="box", hue='Sex')
# boxplot, but also split based on sex

plt.show()
# now it shows all the graphs when the program is run

print('done')