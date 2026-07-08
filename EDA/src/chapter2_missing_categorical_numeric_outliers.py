"""
Missing Data, Categorical & Numeric Data, and Outliers
--------------------------------------------------------
Cleaning up a real-world "data professionals' salaries" dataset: finding and
addressing missing values (drop vs. impute), turning messy free-text job
titles into a small set of categories, converting a string-typed numeric
column into a usable number, and detecting/handling outliers with the
interquartile range (IQR).

Table of Contents
1. Checking for missing values
2. Strategies for addressing missing data
3. Dropping missing values above a threshold
4. Imputing a summary statistic
5. Imputing by sub-group
6. Previewing categorical columns
7. Job titles: value_counts() and nunique()
8. Extracting value from categories with str.contains()
9. Finding multiple phrases with regex
10. Creating a categorical column with np.select()
11. Visualizing categorical frequency: count plots
12. Converting strings to numbers
13. Adding summary statistics into a DataFrame with .transform()
14. Using descriptive statistics and the IQR
15. Identifying thresholds and outliers
16. Dropping outliers
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# salaries is assumed already loaded as a DataFrame of data-professional
# salary records (its read_csv call wasn't captured in the slide extraction).

# =====================================================================
# 1. Checking for missing values
# =====================================================================

# Missing data skews distributions and can misrepresent whole subgroups
# (e.g. dropping the oldest/tallest respondents), leading to wrong
# conclusions. .isna().sum() counts nulls per column.
print(salaries.isna().sum())
# Working_Year            12
# Designation             27
# Experience              33
# Employment_Status       31
# Employee_Location       28
# Company_Size            40
# Remote_Working_Ratio    24
# Salary_USD              60
# dtype: int64


# =====================================================================
# 2. Strategies for addressing missing data
# =====================================================================

# Three common strategies, depending on how much is missing and why:
#   - Drop missing values          (rule of thumb: 5% or less of total values)
#   - Impute mean, median, or mode  (depends on the distribution/context)
#   - Impute by sub-group           (e.g. different experience levels have
#                                    different median salaries)


# =====================================================================
# 3. Dropping missing values above a threshold
# =====================================================================

# A 5%-of-rows threshold decides which sparsely-missing columns are safe
# to drop rows for.
threshold = len(salaries) * 0.05
print(threshold)  # 30

# Columns at or below the threshold of missing values are dropped by row.
cols_to_drop = salaries.columns[salaries.isna().sum() <= threshold]
print(cols_to_drop)
# Index(['Working_Year', 'Designation', 'Employee_Location',
#        'Remote_Working_Ratio'],
#       dtype='object')

salaries.dropna(subset=cols_to_drop, inplace=True)


# =====================================================================
# 4. Imputing a summary statistic
# =====================================================================

# Columns with more missing values (above the threshold) are imputed
# instead of dropped.
cols_with_missing_values = salaries.columns[salaries.isna().sum() > 0]
print(cols_with_missing_values)
# Index(['Experience', 'Employment_Status', 'Company_Size', 'Salary_USD'],
#       dtype='object')

# Impute the mode for every missing column except the last one
# (Salary_USD is numeric and gets a more tailored treatment next).
# NOTE: .fillna() here returns a new Series that isn't captured — to make
# this actually persist you'd need salaries[col] = salaries[col].fillna(...)
# or fillna(..., inplace=True).
for col in cols_with_missing_values[:-1]:
    salaries[col].fillna(salaries[col].mode()[0])


# =====================================================================
# 5. Imputing by sub-group
# =====================================================================

# Checking what's left to impute: only the numeric Salary_USD column.
print(salaries.isna().sum())
# Working_Year             0
# Designation              0
# Experience               0
# Employment_Status        0
# Employee_Location        0
# Company_Size             0
# Remote_Working_Ratio     0
# Salary_USD              41

# Different experience levels have different typical salaries, so impute
# the median salary per sub-group (Experience) rather than one global median.
salaries_dict = salaries.groupby("Experience")["Salary_USD"].median().to_dict()
print(salaries_dict)
# {'Entry': 55380.0, 'Executive': 135439.0, 'Mid': 74173.5, 'Senior': 128903.0}

# .map() looks up each row's Experience in salaries_dict; fillna() uses that
# as the fill value for missing Salary_USD entries.
salaries["Salary_USD"] = salaries["Salary_USD"].fillna(salaries["Experience"].map(salaries_dict))

# No more missing values!
print(salaries.isna().sum())
# Working_Year            0
# Designation             0
# Experience              0
# Employment_Status       0
# Employee_Location       0
# Company_Size            0
# Remote_Working_Ratio    0
# Salary_USD              0
# dtype: int64


# =====================================================================
# 6. Previewing categorical columns
# =====================================================================

# .select_dtypes("object") isolates the text/categorical columns for review.
print(salaries.select_dtypes("object").head())
#   Designation                 Experience Employment_Status Employee_Location Company_Size
# 0 Data Scientist              Mid        FT                DE                L
# 1 Machine Learning Scientist  Senior     FT                JP                S
# 2 Big Data Engineer           Senior     FT                GB                M
# 3 Product Data Analyst        Mid        FT                HN                S
# 4 Machine Learning Engineer   Senior     FT                US                L


# =====================================================================
# 7. Job titles: value_counts() and nunique()
# =====================================================================

# Designation has too many free-text variants to analyze directly.
print(salaries["Designation"].value_counts())
# Data Scientist                              143
# Data Engineer                               132
# Data Analyst                                 97
# Machine Learning Engineer                    41
# Research Scientist                           16
# Data Science Manager                         12
# Data Architect                               11
# Big Data Engineer                             8
# Machine Learning Scientist                    8
# ...

# .nunique() counts how many distinct job titles exist in total.
print(salaries["Designation"].nunique())  # 50


# =====================================================================
# 8. Extracting value from categories with str.contains()
# =====================================================================

# The current free-text format limits our ability to generate insights.
# str.contains() searches a column for a specific string.
print(salaries["Designation"].str.contains("Scientist"))
# 0       True
# 1       True
# 2      False
# 3      False
#        ...
# 604    False
# 605    False
# 606     True
# Name: Designation, Length: 607, dtype: bool


# =====================================================================
# 9. Finding multiple phrases with regex
# =====================================================================

# | (or) matches either phrase, e.g. titles mentioning Machine Learning or AI.
print(salaries["Designation"].str.contains("Machine Learning|AI"))
# 0      False
# 1       True
# 2      False
# 3      False
#        ...
# 604    False
# 605    False
# 606     True
# Name: Designation, Length: 607, dtype: bool

# ^ anchors the match to the start of the string, e.g. titles starting with Data.
print(salaries["Designation"].str.contains("^Data"))
# 0       True
# 1      False
# 2      False
# 3      False
#        ...
# 604     True
# 605     True
# 606    False
# Name: Designation, Length: 607, dtype: bool

# The target set of job categories to bucket every title into.
job_categories = ["Data Science", "Data Analytics",
                   "Data Engineering", "Machine Learning",
                   "Managerial", "Consultant"]

# One regex pattern of matching phrases per category.
data_science = "Data Scientist|NLP"
data_analyst = "Analyst|Analytics"
data_engineer = "Data Engineer|ETL|Architect|Infrastructure"
ml_engineer = "Machine Learning|ML|Big Data|AI"
manager = "Manager|Head|Director|Lead|Principal|Staff"
consultant = "Consultant|Freelance"

# One boolean condition per category, in the same order as job_categories.
conditions = [
    (salaries["Designation"].str.contains(data_science)),
    (salaries["Designation"].str.contains(data_analyst)),
    (salaries["Designation"].str.contains(data_engineer)),
    (salaries["Designation"].str.contains(ml_engineer)),
    (salaries["Designation"].str.contains(manager)),
    (salaries["Designation"].str.contains(consultant))
]


# =====================================================================
# 10. Creating a categorical column with np.select()
# =====================================================================

# np.select() picks the matching job_categories label for the first True
# condition per row, falling back to "Other" if none match.
salaries["Job_Category"] = np.select(conditions,
                                      job_categories,
                                      default="Other")

print(salaries[["Designation", "Job_Category"]].head())
#                   Designation      Job_Category
# 0              Data Scientist      Data Science
# 1  Machine Learning Scientist  Machine Learning
# 2           Big Data Engineer  Data Engineering
# 3        Product Data Analyst    Data Analytics
# 4   Machine Learning Engineer  Machine Learning


# =====================================================================
# 11. Visualizing categorical frequency: count plots
# =====================================================================

# A count plot shows how many rows fall into each Job_Category.
sns.countplot(data=salaries, x="Job_Category")
plt.show()


# =====================================================================
# 12. Converting strings to numbers
# =====================================================================

# This section starts from a rawer version of the salaries dataset, where
# salary is stored as comma-formatted rupee strings instead of a USD float.
print(salaries.info())
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 594 entries, 0 to 593
# Data columns (total 9 columns):
#  #   Column                Non-Null Count  Dtype
#  0   Working_Year          594 non-null    int64
#  1   Designation           567 non-null    object
#  2   Experience            561 non-null    object
#  3   Employment_Status     563 non-null    object
#  4   Salary_In_Rupees      566 non-null    object
#  5   Employee_Location     554 non-null    object
#  6   Company_Location      570 non-null    object
#  7   Company_Size          535 non-null    object
#  8   Remote_Working_Ratio  571 non-null    float64
# dtypes: float64(1), int64(1), object(7)
# memory usage: 41.9+ KB

print(salaries["Salary_In_Rupees"].head())
# 0    20,688,070.00
# 1     8,674,985.00
# 2     1,591,390.00
# 3    11,935,425.00
# 4     5,729,004.00
# Name: Salary_In_Rupees, dtype: object

# To convert: (1) remove the commas, (2) cast to float, (3) derive a new
# column in the target currency.
# pd.Series.str.replace("characters to remove", "characters to replace them with")
salaries["Salary_In_Rupees"] = salaries["Salary_In_Rupees"].str.replace(",", "")
print(salaries["Salary_In_Rupees"].head())
# 0    20688070.00
# 1     8674985.00
# 2     1591390.00
# 3    11935425.00
# 4     5729004.00
# Name: Salary_In_Rupees, dtype: object

salaries["Salary_In_Rupees"] = salaries["Salary_In_Rupees"].astype(float)

# 1 Indian Rupee = 0.012 US Dollars
salaries["Salary_USD"] = salaries["Salary_In_Rupees"] * 0.012

print(salaries[["Salary_In_Rupees", "Salary_USD"]].head())
#    Salary_In_Rupees  Salary_USD
# 0        20688070.0  248256.840
# 1         8674985.0  104099.820
# 2         1591390.0   19096.680
# 3        11935425.0  143225.100
# 4         5729004.0   68748.048


# =====================================================================
# 13. Adding summary statistics into a DataFrame with .transform()
# =====================================================================

# A plain groupby-mean summarizes each Company_Size in its own small table.
print(salaries.groupby("Company_Size")["Salary_USD"].mean())
# Company_Size
# L    111934.432174
# M    110706.628527
# S     69880.980179
# Name: Salary_USD, dtype: float64

# .transform() instead broadcasts the group statistic back onto every row,
# so it can be stored as a new column on the original DataFrame.
salaries["std_dev"] = salaries.groupby("Experience")["Salary_USD"].transform(lambda x: x.std())
print(salaries[["Experience", "std_dev"]].value_counts())
# Experience         std_dev
# SE                 52995.385395        257
# MI                 63217.397343        197
# EN                 43367.256303         83
# EX                 86426.611619         24

# Works the same way for any group/column/statistic combination.
salaries["median_by_comp_size"] = salaries.groupby("Company_Size") \
                                        ["Salary_USD"].transform(lambda x: x.median())
print(salaries[["Company_Size", "median_by_comp_size"]].head())
#   Company_Size  median_by_comp_size
# 0            S            60833.424
# 1            M           105914.964
# 2            S            60833.424
# 3            L            95483.400
# 4            L            95483.400


# =====================================================================
# 14. Using descriptive statistics and the IQR
# =====================================================================

# An outlier is an observation far away from other data points (e.g. a
# median house price of $400,000 vs. an outlier price of $5,000,000) —
# worth investigating why, rather than assuming it's wrong.
print(salaries["Salary_USD"].describe())
# count       518.000
# mean     104905.826
# std       62660.107
# min        3819.000
# 25%       61191.000
# 50%       95483.000
# 75%      137496.000
# max      429675.000
# Name: Salary_USD, dtype: float64

# Interquartile range (IQR) = 75th percentile - 25th percentile.
# A boxplot visualizes the IQR directly (the box) along with outliers
# (the points beyond the whiskers).
sns.boxplot(data=salaries,
            y="Salary_USD")
plt.show()

# Outlier rule of thumb based on the IQR:
#   Upper outliers: value > 75th percentile + (1.5 * IQR)
#   Lower outliers: value < 25th percentile - (1.5 * IQR)


# =====================================================================
# 15. Identifying thresholds and outliers
# =====================================================================

# 75th percentile
seventy_fifth = salaries["Salary_USD"].quantile(0.75)
# 25th percentile
twenty_fifth = salaries["Salary_USD"].quantile(0.25)
# Interquartile range
salaries_iqr = seventy_fifth - twenty_fifth
print(salaries_iqr)  # 76305.0

# Upper threshold
upper = seventy_fifth + (1.5 * salaries_iqr)
# Lower threshold
lower = twenty_fifth - (1.5 * salaries_iqr)
print(upper, lower)  # 251953.5 -53266.5

# Subset to just the rows outside the thresholds, i.e. the outliers.
salaries[(salaries["Salary_USD"] < lower) | (salaries["Salary_USD"] > upper)] \
        [["Experience", "Employee_Location", "Salary_USD"]]
#         Experience    Employee_Location    Salary_USD
# 29      Mid           US                   429675.0
# 67      Mid           US                   257805.0
# 80      Senior        US                   263534.0
# 83      Mid           US                   429675.0
# 133     Mid           US                   403895.0
# 410     Executive     US                   309366.0
# 441     Senior        US                   362837.0
# 445     Senior        US                   386708.0
# 454     Senior        US                   254368.0

# Outliers can change the mean/standard deviation and violate the
# normality assumptions many statistical tests and ML models rely on. Worth
# asking: why do these outliers exist (e.g. more senior roles/countries pay
# more — keep them), or is the data simply wrong (e.g. a collection
# error — drop them)?


# =====================================================================
# 16. Dropping outliers
# =====================================================================

# Keep only the rows within the lower/upper thresholds.
no_outliers = salaries[(salaries["Salary_USD"] > lower) & (salaries["Salary_USD"] < upper)]
print(no_outliers["Salary_USD"].describe())
# count       509.000000
# mean     100674.567780
# std       53643.050057
# min        3819.000000
# 25%       60928.000000
# 50%       95483.000000
# 75%      134059.000000
# max      248257.000000
# Name: Salary_USD, dtype: float64
