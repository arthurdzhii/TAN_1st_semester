"""
Displays data a clean DataProb2 dataset in the form of scatterplots
with linear regression and boxplots for a clean DataProb2 dataset
"""

import pandas as pd
import seaborn as sns   # seaborn package imported with an alias. Used for data visualization based on matplotlib and integrates well with pandas
import matplotlib.pyplot as plt     # pyplot interface from matplotlib package imported

### WORKING WITH THE CLEAN DATASET

exam_df = pd.read_csv("exam_dataset.csv", sep=",")
# read the clean dataset

exam_df_ab = exam_df[(exam_df.Profile == "A") | (exam_df.Profile == "B")]
# instantiating a DataFrame object that only has Profiles with values A or B

sns.lmplot(x="JFC_fitting", y="Speech", col="Profile", data=exam_df_ab)
# scatterplots with linear regression for Profiles A and B, for variables JFC_fitting and Speech
# .lmplot() creates regression models for 2 variables from a DataFrame
# ci is confidence interval of the regression model, the more narrow the better

sns.catplot(data=exam_df_ab, x="Profile", y="Speech", kind="box", hue='RespRateLevel')
# figure with four box plots, one for each combination of factors, that is A-low, A-high, B-low and B-high
# Speech chosen randomly as the other variable, could be any other

plt.show()
# method from the matplotlib package that displays all open figures when the program runs

print("Here are your charts!")
