"""
Patterns Over Time, Correlation, and Factor Relationships
------------------------------------------------------------
Working with a "divorce" dataset to explore time-based patterns (parsing
and deriving DateTime columns, plotting a trend over time), quantifying
relationships between numerical variables with correlation and heatmaps,
and exploring how a relationship or distribution differs across a
categorical factor with histograms, KDE plots, and scatter plots.

Table of Contents
1. Importing and creating DateTime data
2. Extracting DateTime parts with dt attributes
3. Visualizing patterns over time: line plots
4. Correlation with .corr()
5. Correlation heatmaps
6. Correlation in context: date ranges and non-linear relationships
7. Scatter plots and pairplots
8. Categorical value counts
9. Exploring categorical relationships: histograms with hue
10. Kernel Density Estimate (KDE) plots
11. Cumulative KDE plots
12. Deriving an age-at-marriage feature
13. Scatter plots with categorical variables
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =====================================================================
# 1. Importing and creating DateTime data
# =====================================================================

divorce = pd.read_csv("divorce.csv")
print(divorce.head())
#   marriage_date  marriage_duration
# 0    2000-06-26                5.0
# 1    2000-02-02                2.0
# 2    1991-10-09               10.0
# 3    1993-01-02               10.0
# 4    1998-12-11                7.0

# DateTime data needs to be explicitly declared to pandas — by default a
# date column like this is read in as a plain object (string).
print(divorce.dtypes)
# marriage_date         object
# marriage_duration    float64
# dtype: object

# parse_dates tells read_csv() which column(s) to parse as DateTime on load.
divorce = pd.read_csv("divorce.csv", parse_dates=["marriage_date"])
print(divorce.dtypes)
# marriage_date        datetime64[ns]
# marriage_duration           float64
# dtype: object

# pd.to_datetime() converts an existing column to DateTime after the fact.
divorce["marriage_date"] = pd.to_datetime(divorce["marriage_date"])
print(divorce.dtypes)
# marriage_date        datetime64[ns]
# marriage_duration           float64
# dtype: object

# pd.to_datetime() can also build a DateTime column out of separate
# month/day/year columns.
print(divorce.head(2))
#    month  day  year  marriage_duration
# 0      6   26  2000                5.0
# 1      2    2  2000                2.0

divorce["marriage_date"] = pd.to_datetime(divorce[["month", "day", "year"]])
print(divorce.head(2))
#    month  day  year  marriage_duration marriage_date
# 0      6   26  2000                5.0    2000-06-26
# 1      2    2  2000                2.0    2000-02-02


# =====================================================================
# 2. Extracting DateTime parts with dt attributes
# =====================================================================

# Once a column is DateTime, dt.month/dt.day/dt.year extract each part.
divorce["marriage_month"] = divorce["marriage_date"].dt.month
print(divorce.head())
#   marriage_date  marriage_duration  marriage_month
# 0    2000-06-26                5.0               6
# 1    2000-02-02                2.0               2
# 2    1991-10-09               10.0              10
# 3    1993-01-02               10.0               1
# 4    1998-12-11                7.0              12


# =====================================================================
# 3. Visualizing patterns over time: line plots
# =====================================================================

# A line plot shows how a numerical variable changes across an ordered
# (e.g. time-based) x-axis.
sns.lineplot(data=divorce, x="marriage_month", y="marriage_duration")
plt.show()


# =====================================================================
# 4. Correlation with .corr()
# =====================================================================

# Correlation describes the direction and strength of the relationship
# between two numerical variables. numeric_only=True skips non-numeric
# columns so they don't raise an error.
print(divorce.corr(numeric_only=True))
#                     income_man  income_woman  marriage_duration  num_kids  marriage_year
# income_man               1.000         0.318              0.085     0.041          0.019
# income_woman             0.318         1.000              0.079    -0.018          0.026
# marriage_duration        0.085         0.079              1.000     0.447         -0.812
# num_kids                 0.041        -0.018              0.447     1.000         -0.461
# marriage_year            0.019         0.026             -0.812    -0.461          1.000
# .corr() calculates the Pearson correlation coefficient by default.


# =====================================================================
# 5. Correlation heatmaps
# =====================================================================

# A heatmap makes a correlation matrix much easier to scan; annot=True
# prints each coefficient inside its cell.
sns.heatmap(divorce.corr(numeric_only=True), annot=True)
plt.show()


# =====================================================================
# 6. Correlation in context: date ranges and non-linear relationships
# =====================================================================

# Always check the underlying date range before interpreting a correlation.
print(divorce["divorce_date"].min())  # Timestamp('2000-01-08 00:00:00')
print(divorce["divorce_date"].max())  # Timestamp('2015-11-03 00:00:00')

# Correlation only measures LINEAR relationships — a strong non-linear
# relationship can still have a Pearson coefficient near zero.
# Example: a strong but non-linear relationship -> coefficient -6.48e-18
# Example: a quadratic relationship (not linear) -> coefficient .971211


# =====================================================================
# 7. Scatter plots and pairplots
# =====================================================================

# A scatter plot visualizes the relationship between two numerical
# variables directly.
sns.scatterplot(data=divorce, x="income_man", y="income_woman")
plt.show()

# A pairplot draws scatter plots (and histograms) for every pair of
# numerical columns in the DataFrame at once.
sns.pairplot(data=divorce)
plt.show()

# vars restricts a pairplot to a chosen subset of columns.
sns.pairplot(data=divorce, vars=["income_man", "income_woman", "marriage_duration"])
plt.show()


# =====================================================================
# 8. Categorical value counts
# =====================================================================

# Before exploring a categorical relationship, check the category
# frequencies for the factor of interest.
print(divorce["education_man"].value_counts())
# Professional    1313
# Preparatory      501
# Secondary        288
# Primary          100
# None               4
# Other               3
# Name: education_man, dtype: int64


# =====================================================================
# 9. Exploring categorical relationships: histograms with hue
# =====================================================================

# A plain histogram shows the overall distribution.
sns.histplot(data=divorce, x="marriage_duration", binwidth=1)
plt.show()

# hue splits the histogram into one distribution per category, revealing
# how the factor relates to the numerical variable.
sns.histplot(data=divorce, x="marriage_duration", hue="education_man", binwidth=1)
plt.show()


# =====================================================================
# 10. Kernel Density Estimate (KDE) plots
# =====================================================================

# A KDE plot is a smoothed version of a histogram, useful for comparing
# distribution shapes across categories.
sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man")
plt.show()

# By default a KDE can extend past the actual data range (e.g. below 0);
# cut=0 clips the curve to the observed data range.
sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man", cut=0)
plt.show()


# =====================================================================
# 11. Cumulative KDE plots
# =====================================================================

# cumulative=True plots the cumulative distribution instead of the density,
# useful for reading off "what fraction of marriages lasted less than X".
sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man", cut=0, cumulative=True)
plt.show()


# =====================================================================
# 12. Deriving an age-at-marriage feature
# =====================================================================

# Is there a relationship between age at marriage and education level?
# Derive it from the marriage year and each partner's birth year.
divorce["man_age_marriage"] = divorce["marriage_year"] - divorce["dob_man"].dt.year
divorce["woman_age_marriage"] = divorce["marriage_year"] - divorce["dob_woman"].dt.year


# =====================================================================
# 13. Scatter plots with categorical variables
# =====================================================================

sns.scatterplot(data=divorce, x="woman_age_marriage", y="man_age_marriage")
plt.show()

# hue overlays the categorical factor (education level) onto the scatter
# plot of the two numerical variables.
sns.scatterplot(data=divorce,
                x="woman_age_marriage",
                y="man_age_marriage",
                hue="education_man")
plt.show()
