"""Program that loads and cleans DataProb2.csv and saves the clean dataset in a new csv file"""

import pandas as pd     # pandas package imported with an alias. Used for reading csv file and working with DataFrame

### CLEANING THE DATA

exam_df = pd.read_csv('DataProb2.csv', delimiter=";")
# function to read csv files as DataFrame objects
# file path of an existing file given. Delimiter is how data is separated in the csv file, it could also be "," fx

description = exam_df.describe()
# creates a DataFrame with descriptive statistics
# multiple categories with missing values
# max values in JFC and HINT are outliers
# profile has undefined values
# NumbAnswers and LogPeriod could have some outlier values

exam_df = exam_df.drop_duplicates()
# a good safety measure, although there are no duplicates in this dataset

exam_df.isnull().any()
# 9 categories have missing values
exam_df = exam_df.dropna(axis=0, how='any')
# .dropna() method removes missing values
# axis = 0 means rows (1 would be columns)
# how="any" means that the row is removed if there is at least one empty value
# both parameters are defaults, so there was no need to specify them here

exam_df.groupby('JFC_fitting').agg({'JFC_fitting':['count']})
exam_df.groupby('HINT_fitting').agg({'HINT_fitting':['count']})
# .groupby() and .agg() methods are used together
# .agg() counts how many condition values are in each group
# each variable has one outlier value of 999.0 that needs to be removed
exam_df = exam_df[(exam_df.JFC_fitting<5) & (exam_df.HINT_fitting<5)]
# Series intersection between legal JFC and HINT values
# one row is removed

exam_df.groupby('Profile').agg({'Profile':['count']})
# 2 undefined values for Profile, the rest are A B C D
exam_df = exam_df[(exam_df.Profile=="A") | (exam_df.Profile=="B") | (exam_df.Profile=="C") | (exam_df.Profile=="D")]
# Series union with profiles A B C and D
# the 2 rows with undefined Profile values are removed

exam_df.groupby('NumbAnswers').agg({'NumbAnswers':['count']})
exam_df.groupby('LogPeriod').agg({'LogPeriod':['count']})
# NumbAnswers have some numbers above 2000, but I decided not to clean them, because I dont know what this data represents
# LogPeriod has one value significantly above 100 (147), which could be an outlier
exam_df = exam_df[(exam_df.LogPeriod<=100)]
# one row removed

exam_df["RespRateLevel"] = pd.cut(exam_df["RespRate"], bins=[0, 0.2, 1], labels=["low", "high"])
# creating a new ordinal categorical variable RespRateLevel and adding it to the DataFrame
# .cut() method takes an array (a variable "RespRate" from the DataFrame in this case)
# bins must always be 1 more than labels
# third bin could be float("Inf"), but in this dataset there are no values > 1
# this variable later used for visualization

description = exam_df.describe()
# check the descriptive DataFrame again, data looks much cleaner

exam_df.to_csv("exam_dataset.csv", sep=",")
# saving the cleaned dataset to a new csv file
# sep="," because I like it better that way

print("Your data is cleaned!")
