"""
Initial Exploration, Validation & Summarization
------------------------------------------------
The first steps of Exploratory Data Analysis (EDA): getting a first look at
a new DataFrame, checking that its data types and category/number ranges
make sense, and summarizing it numerically (with .groupby()/.agg()) and
visually (with seaborn histograms, boxplots, and bar plots).

Table of Contents
1. A first look with .head() and .info()
2. Categorical columns: .value_counts()
3. Numerical columns: .describe()
4. Visualizing numerical data: histograms
5. Validating data types
6. Validating categorical data with .isin()
7. Validating numerical data: min(), max(), and boxplots
8. Exploring groups of data with .groupby()
9. Aggregating functions
10. Aggregating ungrouped data with .agg()
11. Named summary columns
12. Visualizing categorical summaries: bar plots
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =====================================================================
# 1. A first look with .head() and .info()
# =====================================================================

# .head() previews the first 5 rows of a DataFrame.
books = pd.read_csv("books.csv")
print(books.head())
#                              name                     author  rating  year        genre
# 0  10-Day Green Smoothie Cleanse                   JJ Smith    4.73  2016  Non Fiction
# 1              11/22/63: A Novel               Stephen King    4.62  2011      Fiction
# 2              12 Rules for Life         Jordan B. Peterson    4.69  2018  Non Fiction
# 3         1984 (Signet Classics)              George Orwell    4.73  2017      Fiction
# 4           5,000 Awesome Facts   National Geographic Kids    4.81  2019    Childrens

# .info() reports row/column counts, non-null counts, and dtypes at once.
print(books.info())
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 350 entries, 0 to 349
# Data columns (total 5 columns):
#  #   Column  Non-Null Count  Dtype
#  0   name    350 non-null    object
#  1   author  350 non-null    object
#  2   rating  350 non-null    float64
#  3   year    350 non-null    int64
#  4   genre   350 non-null    object
# dtypes: float64(1), int64(1), object(3)
# memory usage: 13.8+ KB


# =====================================================================
# 2. Categorical columns: .value_counts()
# =====================================================================

# .value_counts() on a categorical column shows the count of each category.
print(books.value_counts("genre"))
# genre
# Non Fiction    179
# Fiction        131
# Childrens       40
# dtype: int64


# =====================================================================
# 3. Numerical columns: .describe()
# =====================================================================

# .describe() summarizes numerical columns: count, mean, std, min/max, quartiles.
print(books.describe())
#          rating        year
# count    350.000000  350.000000
# mean       4.608571  2013.508571
# std        0.226941     3.284711
# min        3.300000  2009.000000
# 25%        4.500000  2010.000000
# 50%        4.600000  2013.000000
# 75%        4.800000  2016.000000
# max        4.900000  2019.000000


# =====================================================================
# 4. Visualizing numerical data: histograms
# =====================================================================

# A histogram shows the distribution shape of a numerical column.
sns.histplot(data=books, x="rating")
plt.show()

# binwidth controls how finely the values are bucketed.
sns.histplot(data=books, x="rating", binwidth=.1)
plt.show()


# =====================================================================
# 5. Validating data types
# =====================================================================

# .dtypes reports the column dtypes directly, without the rest of .info().
print(books.dtypes)
# name       object
# author     object
# rating    float64
# year      float64   <- should be int64, was read in as float
# genre      object
# dtype: object

# astype() converts a column to a different, more appropriate dtype.
books["year"] = books["year"].astype(int)
print(books.dtypes)
# name       object
# author     object
# rating    float64
# year        int64
# genre      object
# dtype: object

# Reference: common Python types and their names, for use with astype().
#   String     -> str
#   Integer    -> int
#   Float      -> float
#   Dictionary -> dict
#   List       -> list
#   Boolean    -> bool


# =====================================================================
# 6. Validating categorical data with .isin()
# =====================================================================

# .isin() checks each value against a list of valid categories.
print(books["genre"].isin(["Fiction", "Non Fiction"]))
# 0       True
# 1       True
# 2       True
# 3       True
# 4      False
#        ...
# 345     True
# 346     True
# 347     True
# 348     True
# 349    False
# Name: genre, Length: 350, dtype: bool

# ~ negates the boolean Series, flagging rows that do NOT match.
print(~books["genre"].isin(["Fiction", "Non Fiction"]))
# 0      False
# 1      False
# 2      False
# 3      False
# 4       True
#        ...
# 345    False
# 346    False
# 347    False
# 348    False
# 349     True
# Name: genre, Length: 350, dtype: bool

# The boolean Series can be used directly to subset rows.
print(books[books["genre"].isin(["Fiction", "Non Fiction"])].head())
#    name                            author                rating  year  genre
# 0  10-Day Green Smoothie Cleanse    JJ Smith               4.7  2016  Non Fiction
# 1  11/22/63: A Novel                Stephen King           4.6  2011      Fiction
# 2  12 Rules for Life                Jordan B. Peterson     4.7  2018  Non Fiction
# 3  1984 (Signet Classics)           George Orwell          4.7  2017      Fiction
# 5  A Dance with Dragons              George R. R. Martin   4.4  2011      Fiction


# =====================================================================
# 7. Validating numerical data: min(), max(), and boxplots
# =====================================================================

# .select_dtypes() picks out only the numerical columns.
print(books.select_dtypes("number").head())
#    rating  year
# 0     4.7  2016
# 1     4.6  2011
# 2     4.7  2018
# 3     4.7  2017
# 4     4.8  2019

# .min() and .max() report the smallest/largest value for a range check.
print(books["year"].min())  # 2009
print(books["year"].max())  # 2019

# A boxplot visualizes the range/spread of a numerical column.
sns.boxplot(data=books, x="year")
plt.show()

# Passing a categorical y groups the boxplot by category.
sns.boxplot(data=books, x="year", y="genre")
plt.show()


# =====================================================================
# 8. Exploring groups of data with .groupby()
# =====================================================================

# .groupby() groups rows by category; the aggregating function (here mean())
# says how to summarize each group.
print(books[["genre", "rating", "year"]].groupby("genre").mean())
#                rating         year
# genre
# Childrens    4.780000  2015.075000
# Fiction      4.570229  2013.022901
# Non Fiction  4.598324  2013.513966


# =====================================================================
# 9. Aggregating functions
# =====================================================================

# Common aggregating functions available on a grouped DataFrame:
#   Sum               -> .sum()
#   Count             -> .count()
#   Minimum           -> .min()
#   Maximum           -> .max()
#   Variance          -> .var()
#   Standard deviation -> .std()


# =====================================================================
# 10. Aggregating ungrouped data with .agg()
# =====================================================================

# .agg() applies one or more aggregating functions across a DataFrame at once.
print(books[["rating", "year"]].agg(["mean", "std"]))
#         rating        year
# mean  4.608571  2013.508571
# std   0.226941     3.28471


# =====================================================================
# 11. Named summary columns
# =====================================================================

# A dict passed to .agg() applies different functions to different columns.
print(books.agg({"rating": ["mean", "std"], "year": ["median"]}))
#          rating    year
# mean    4.608571     NaN
# std     0.226941     NaN
# median       NaN  2013.0

# Passing name=(column, function) pairs to .agg() on a grouped DataFrame
# produces custom-named summary columns.
print(books.groupby("genre").agg(
    mean_rating=("rating", "mean"),
    std_rating=("rating", "std"),
    median_year=("year", "median")
))
#              mean_rating  std_rating  median_year
# genre
# Childrens       4.780000    0.122370       2015.0
# Fiction         4.570229    0.281123       2013.0
# Non Fiction     4.598324    0.179411       2013.0


# =====================================================================
# 12. Visualizing categorical summaries: bar plots
# =====================================================================

# A bar plot shows a summary statistic (mean by default) of a numerical
# column, broken out by category.
sns.barplot(data=books, x="genre", y="rating")
plt.show()
