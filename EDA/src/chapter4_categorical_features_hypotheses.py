"""
Categorical Data Considerations, Feature Generation & Hypotheses
--------------------------------------------------------------------
Working with a flight-price ("planes") dataset to reason about whether a
sample is representative, cross-tabulate categorical variables, engineer
new numerical/categorical features (cleaned stop counts, date/time parts,
price bands), and use correlation and grouped plots to generate — not yet
test — hypotheses about what drives ticket price. Closes with a recap of
the whole course.

Table of Contents
1. Why perform EDA, and representative data
2. Categorical classes and class imbalance
3. Class frequency: value_counts() and relative frequency
4. Cross-tabulation with pd.crosstab()
5. Aggregated values with pd.crosstab()
6. Correlation and viewing data types
7. Cleaning the Total_Stops column
8. Extracting date and time features
9. Creating price categories with pd.cut()
10. Visualizing price category by airline
11. Generating hypotheses: spurious correlation and data snooping
12. Bar plots for hypothesis generation
13. Course recap
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =====================================================================
# 1. Why perform EDA, and representative data
# =====================================================================

# EDA is useful for detecting patterns and relationships, generating
# questions/hypotheses, and preparing data for machine learning.
#
# A sample is only useful if it's representative of the population you
# care about — e.g. studying education vs. income in the USA can't rely
# on data collected only in France.


# =====================================================================
# 2. Categorical classes and class imbalance
# =====================================================================

# Categorical classes are just labels, e.g. marital status:
#   Single, Married, Divorced
# Class imbalance is when some classes are far more frequent than others
# in the sample.


# =====================================================================
# 3. Class frequency: value_counts() and relative frequency
# =====================================================================

# .value_counts() shows the raw count of each class.
print(planes["Destination"].value_counts())
# Cochin       4391
# Banglore     2773
# Delhi        1219
# New Delhi     888
# Hyderabad     673
# Kolkata       369
# Name: Destination, dtype: int64

# normalize=True converts counts to a proportion of the whole, e.g. 40% of
# internal Indian flights have a destination of Delhi. Comparing this to
# what's known about the population checks representativeness.
print(planes["Destination"].value_counts(normalize=True))
# Cochin       0.425773
# Banglore     0.268884
# Delhi        0.118200
# New Delhi    0.086105
# Hyderabad    0.065257
# Kolkata      0.035780
# Name: Destination, dtype: float64


# =====================================================================
# 4. Cross-tabulation with pd.crosstab()
# =====================================================================

# pd.crosstab(index, columns) counts how often each pair of category
# values co-occurs.
print(pd.crosstab(planes["Source"], planes["Destination"]))
# Destination  Banglore  Cochin  Delhi  Hyderabad  Kolkata  New Delhi
# Source
# Banglore            0       0   1199          0        0        868
# Chennai             0       0      0          0      364          0
# Delhi               0    4318      0          0        0          0
# Kolkata          2720       0      0          0        0          0
# Mumbai              0       0      0        662        0          0


# =====================================================================
# 5. Aggregated values with pd.crosstab()
# =====================================================================

# values + aggfunc summarize a third column (instead of just counting)
# for each Source/Destination pair.
print(pd.crosstab(planes["Source"], planes["Destination"],
                   values=planes["Price"], aggfunc="median"))
# Destination  Banglore   Cochin   Delhi  Hyderabad  Kolkata  New Delhi
# Source
# Banglore          NaN      NaN  4823.0        NaN      NaN    10976.5
# Chennai           NaN      NaN     NaN        NaN   3850.0        NaN
# Delhi             NaN  10262.0     NaN        NaN      NaN        NaN
# Kolkata        9345.0      NaN     NaN        NaN      NaN        NaN
# Mumbai            NaN      NaN     NaN     3342.0      NaN        NaN

# Comparing this aggregated sample median against known population medians
# for the same routes is another way to sanity-check representativeness.


# =====================================================================
# 6. Correlation and viewing data types
# =====================================================================

# A correlation heatmap over the numerical columns is a quick first pass
# at spotting relationships worth engineering features around.
sns.heatmap(planes.corr(numeric_only=True), annot=True)
plt.show()

print(planes.dtypes)
# Airline                    object
# Date_of_Journey    datetime64[ns]
# Source                     object
# Destination                object
# Route                      object
# Dep_Time           datetime64[ns]
# Arrival_Time       datetime64[ns]
# Duration                  float64
# Total_Stops                object
# Additional_Info            object
# Price                     float64
# dtype: object


# =====================================================================
# 7. Cleaning the Total_Stops column
# =====================================================================

# Total_Stops is numeric in meaning but stored as text, so it's excluded
# from numeric correlation until it's cleaned.
print(planes["Total_Stops"].value_counts())
# 1 stop      4107
# non-stop    2584
# 2 stops     1127
# 3 stops       29
# 4 stops        1
# Name: Total_Stops, dtype: int64

# Strip the " stops"/" stop" suffixes, replace "non-stop" with "0", then
# convert the whole column to int.
planes["Total_Stops"] = planes["Total_Stops"].str.replace(" stops", "")
planes["Total_Stops"] = planes["Total_Stops"].str.replace(" stop", "")
planes["Total_Stops"] = planes["Total_Stops"].str.replace("non-stop", "0")
planes["Total_Stops"] = planes["Total_Stops"].astype(int)

# Total_Stops is now numeric, so it shows up in the correlation heatmap.
sns.heatmap(planes.corr(numeric_only=True), annot=True)
plt.show()

print(planes.dtypes)
# Airline                    object
# Date_of_Journey    datetime64[ns]
# Source                     object
# Destination                object
# Route                      object
# Dep_Time           datetime64[ns]
# Arrival_Time       datetime64[ns]
# Duration                  float64
# Total_Stops                 int64
# Additional_Info            object
# Price                     float64
# dtype: object


# =====================================================================
# 8. Extracting date and time features
# =====================================================================

# dt.month/dt.weekday pull calendar parts out of a DateTime column.
planes["month"] = planes["Date_of_Journey"].dt.month
planes["weekday"] = planes["Date_of_Journey"].dt.weekday
print(planes[["month", "weekday", "Date_of_Journey"]].head())
#    month  weekday Date_of_Journey
# 0      9        4      2019-09-06
# 1     12        3      2019-12-05
# 2      1        3      2019-01-03
# 3      6        0      2019-06-24
# 4     12        1      2019-12-03

# dt.hour similarly pulls the hour out of a DateTime-typed time column.
planes["Dep_Hour"] = planes["Dep_Time"].dt.hour
planes["Arrival_Hour"] = planes["Arrival_Time"].dt.hour


# =====================================================================
# 9. Creating price categories with pd.cut()
# =====================================================================

# Quartiles of Price define the boundaries of four ticket-type bands.
print(planes["Price"].describe())
# count     7848.000000
# mean      9035.413609
# std       4429.822081
# min       1759.000000
# 25%       5228.000000
# 50%       8355.000000
# 75%      12373.000000
# max      54826.000000
# Name: Price, dtype: float64
#
# Range                Ticket Type
# <= 5228              Economy
# > 5228,  <= 8355      Premium Economy
# > 8355,  <= 12373     Business Class
# > 12373               First Class

twenty_fifth = planes["Price"].quantile(0.25)
median = planes["Price"].median()
seventy_fifth = planes["Price"].quantile(0.75)
maximum = planes["Price"].max()

# labels and bins line up: bins define the edges, labels name each interval.
labels = ["Economy", "Premium Economy", "Business Class", "First Class"]
bins = [0, twenty_fifth, median, seventy_fifth, maximum]

# pd.cut() buckets each Price into the matching labeled band.
planes["Price_Category"] = pd.cut(planes["Price"],
                                   labels=labels,
                                   bins=bins)

print(planes[["Price", "Price_Category"]].head())
#      Price   Price_Category
# 0  13882.0      First Class
# 1   6218.0  Premium Economy
# 2  13302.0      First Class
# 3   3873.0          Economy
# 4  11087.0   Business Class


# =====================================================================
# 10. Visualizing price category by airline
# =====================================================================

# hue breaks each airline's bar into its Price_Category composition.
sns.countplot(data=planes, x="Airline", hue="Price_Category")
plt.show()


# =====================================================================
# 11. Generating hypotheses: spurious correlation and data snooping
# =====================================================================

# Revisit the correlation heatmap now that Total_Stops and the price bands
# exist, to see what "we know" so far.
sns.heatmap(planes.corr(numeric_only=True), annot=True)
plt.show()

# hue can reveal that an apparent relationship is driven by a third,
# confounding variable — a spurious correlation.
sns.scatterplot(data=planes, x="Duration", y="Price", hue="Total_Stops")
plt.show()

# Would data from a different time period give the same results? Detecting
# real relationships/differences/patterns (rather than one-off noise)
# requires hypothesis testing: generating a hypothesis/question and
# deciding on a statistical test BEFORE collecting more data.
#
# Data snooping — testing many hypotheses against the same data you used
# to generate them — inflates the chance of a false positive, so
# hypotheses generated during EDA should be tested on new data.


# =====================================================================
# 12. Bar plots for hypothesis generation
# =====================================================================

# Bar plots comparing a numerical variable across categories are a natural
# way to surface candidate hypotheses (e.g. "does Airline affect Duration?").
sns.barplot(data=planes, x="Airline", y="Duration")
plt.show()

sns.barplot(data=planes, x="Destination", y="Price")
plt.show()

# Next steps for turning a hypothesis into a real test: design the
# experiment (choose a sample, calculate how many data points are needed,
# and decide what statistical test to run).


# =====================================================================
# 13. Course recap
# =====================================================================

# The techniques covered across all four chapters, in one place:
#   - Inspection and validation:    books["year"] = books["year"].astype(int)
#   - Aggregation:                  books.groupby("genre").agg(mean_rating=("rating", "mean"), ...)
#   - Addressing missing data:      salaries.isna().sum(); fillna(); groupby().median()
#   - Analyzing categorical data:   np.select(conditions, job_categories, default="Other")
#   - Applying lambda functions:    salaries.groupby("Experience")["Salary_USD"].transform(lambda x: x.std())
#   - Handling outliers:            sns.boxplot(data=salaries, y="Salary_USD")
#   - Patterns over time:           sns.lineplot(data=divorce, x="marriage_month", y="marriage_duration")
#   - Correlation:                  sns.heatmap(divorce.corr(numeric_only=True), annot=True)
#   - Distributions:                sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man", cut=0)
#   - Cross-tabulation:             pd.crosstab(planes["Source"], planes["Destination"], values=planes["Price"], aggfunc="median")
#   - Generating features:          pd.cut(planes["Price"], labels=labels, bins=bins)
#   - Generating hypotheses:        sns.barplot(data=planes, x="Airline", y="Duration")
#
# Suggested next courses: Sampling in Python, Hypothesis Testing in Python,
# and Supervised Learning with scikit-learn.
