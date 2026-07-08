"""
Creating and Visualizing DataFrames
-------------------------------------
The last chapter closes the loop: visualizing a DataFrame's columns with
Matplotlib-backed plotting methods, finding and handling missing values,
building a DataFrame from scratch out of plain Python dictionaries/lists,
and reading and writing CSV files.

Table of Contents
1. Histograms
2. Bar plots
3. Line plots and rotating axis labels
4. Scatter plots
5. Layering plots: legends and transparency
6. Detecting missing values
7. Removing and replacing missing values
8. Creating DataFrames: list of dictionaries vs. dictionary of lists
9. Reading and writing CSVs
10. Wrap-up
"""

import pandas as pd
import matplotlib.pyplot as plt

# A bigger dog dataset used throughout this chapter's plotting examples —
# too large to type out row by row, so it's loaded from its own CSV.
dog_pack = pd.read_csv("dog_pack.csv")

# =====================================================================
# 1. Histograms
# =====================================================================

# .hist() plots the distribution of a numerical column.
dog_pack["height_cm"].hist()
plt.show()

# bins controls how many bars the values are grouped into.
dog_pack["height_cm"].hist(bins=20)
plt.show()

dog_pack["height_cm"].hist(bins=5)
plt.show()


# =====================================================================
# 2. Bar plots
# =====================================================================

# A bar plot shows the relationship between a categorical variable and a
# numerical variable — here, mean weight per breed.
avg_weight_by_breed = dog_pack.groupby("breed")["weight_kg"].mean()
print(avg_weight_by_breed)
# breed
# Beagle         10.636364
# Boxer          30.620000
# Chihuahua       1.491667
# Chow Chow      22.535714
# Dachshund       9.975000
# Labrador       31.850000
# Poodle         20.400000
# St. Bernard    71.576923
# Name: weight_kg, dtype: float64

# .plot(kind="bar") turns that Series straight into a bar chart.
avg_weight_by_breed.plot(kind="bar")
plt.show()

# title adds a chart title.
avg_weight_by_breed.plot(kind="bar", title="Mean Weight by Dog Breed")
plt.show()


# =====================================================================
# 3. Line plots and rotating axis labels
# =====================================================================

# sully tracks one dog's weight over time — loaded from its own CSV since
# only its first few rows are shown on the slides.
sully = pd.read_csv("sully.csv", parse_dates=["date"])
print(sully.head())
#           date    weight_kg
# 0   2019-01-31         36.1
# 1   2019-02-28         35.3
# 2   2019-03-31         32.0
# 3   2019-04-30         32.9
# 4   2019-05-31         32.0

# kind="line" plots weight over time, connecting the points in order.
sully.plot(x="date", y="weight_kg", kind="line")
plt.show()

# rot rotates the x-axis tick labels, useful when they'd otherwise overlap.
sully.plot(x="date", y="weight_kg", kind="line", rot=45)
plt.show()


# =====================================================================
# 4. Scatter plots
# =====================================================================

# kind="scatter" shows the relationship between two numerical variables.
dog_pack.plot(x="height_cm", y="weight_kg", kind="scatter")
plt.show()


# =====================================================================
# 5. Layering plots: legends and transparency
# =====================================================================

# Calling two plotting methods before plt.show() layers them on the same axes —
# here, one histogram per sex, both height_cm.
dog_pack[dog_pack["sex"] == "F"]["height_cm"].hist()
dog_pack[dog_pack["sex"] == "M"]["height_cm"].hist()
plt.show()

# plt.legend() labels which plotted series is which.
dog_pack[dog_pack["sex"] == "F"]["height_cm"].hist()
dog_pack[dog_pack["sex"] == "M"]["height_cm"].hist()
plt.legend(["F", "M"])
plt.show()

# alpha makes overlapping bars partially see-through.
dog_pack[dog_pack["sex"] == "F"]["height_cm"].hist(alpha=0.7)
dog_pack[dog_pack["sex"] == "M"]["height_cm"].hist(alpha=0.7)
plt.legend(["F", "M"])
plt.show()

# The avocados dataset used in this chapter's plotting exercises — 1014
# rows, far too many to reproduce here, so it's loaded from its own CSV.
avocados = pd.read_csv("avocados.csv", parse_dates=["date"])
print(avocados)
#             date          type  year  avg_price         size     nb_sold
# 0     2015-12-27  conventional  2015       0.95        small  9626901.09
# 1     2015-12-20  conventional  2015       0.98        small  8710021.76
# 2     2015-12-13  conventional  2015       0.93        small  9855053.66
# ...          ...           ...   ...        ...          ...         ...
# 1011  2018-01-21       organic  2018       1.63  extra_large     1490.02
# 1012  2018-01-14       organic  2018       1.59  extra_large     1580.01
# 1013  2018-01-07       organic  2018       1.51  extra_large     1289.07
#
# [1014 rows x 6 columns]


# =====================================================================
# 6. Detecting missing values
# =====================================================================

# The dogs DataFrame here has a couple of missing weight_kg values.
dogs = pd.DataFrame({
    "name": ["Bella", "Charlie", "Lucy", "Cooper", "Max", "Stella", "Bernie"],
    "breed": ["Labrador", "Poodle", "Chow Chow", "Schnauzer", "Labrador",
              "Chihuahua", "St. Bernard"],
    "color": ["Brown", "Black", "Brown", "Gray", "Black", "Tan", "White"],
    "height_cm": [56, 43, 46, 49, 59, 18, 77],
    "weight_kg": [None, 24.0, 24.0, None, 29.0, 2.0, 74.0],
    "date_of_birth": ["2013-07-01", "2016-09-16", "2014-08-25", "2011-12-11",
                       "2017-01-20", "2015-04-20", "2018-02-27"],
})
print(dogs)
#       name        breed  color  height_cm  weight_kg date_of_birth
# 0    Bella     Labrador  Brown         56        NaN    2013-07-01
# 1  Charlie       Poodle  Black         43       24.0    2016-09-16
# 2     Lucy    Chow Chow  Brown         46       24.0    2014-08-25
# 3   Cooper    Schnauzer   Gray         49        NaN    2011-12-11
# 4      Max     Labrador  Black         59       29.0    2017-01-20
# 5   Stella    Chihuahua    Tan         18        2.0    2015-04-20
# 6   Bernie  St. Bernard  White         77       74.0    2018-02-27

# .isna() flags every individual missing cell.
print(dogs.isna())
#     name  breed  color  height_cm  weight_kg  date_of_birth
# 0  False  False  False      False       True          False
# 1  False  False  False      False      False          False
# 2  False  False  False      False      False          False
# 3  False  False  False      False       True          False
# 4  False  False  False      False      False          False
# 5  False  False  False      False      False          False
# 6  False  False  False      False      False          False

# .isna().any() collapses that down to one flag per column.
print(dogs.isna().any())
# name             False
# breed            False
# color            False
# height_cm        False
# weight_kg         True
# date_of_birth    False
# dtype: bool

# .isna().sum() counts missing values per column instead.
print(dogs.isna().sum())
# name             0
# breed            0
# color            0
# height_cm        0
# weight_kg        2
# date_of_birth    0
# dtype: int64

# The missing-value counts can be plotted directly, since they're just a Series.
dogs.isna().sum().plot(kind="bar")
plt.show()


# =====================================================================
# 7. Removing and replacing missing values
# =====================================================================

# .dropna() drops every row that has at least one missing value.
print(dogs.dropna())
#       name        breed  color  height_cm  weight_kg date_of_birth
# 1  Charlie       Poodle  Black         43       24.0    2016-09-16
# 2     Lucy    Chow Chow  Brown         46       24.0    2014-08-25
# 4      Max     Labrador  Black         59       29.0    2017-01-20
# 5   Stella    Chihuahua    Tan         18        2.0    2015-04-20
# 6   Bernie  St. Bernard  White         77       74.0    2018-02-27

# .fillna() replaces missing values with a given value instead of dropping rows.
print(dogs.fillna(0))
#       name        breed  color  height_cm  weight_kg date_of_birth
# 0    Bella     Labrador  Brown         56        0.0    2013-07-01
# 1  Charlie       Poodle  Black         43       24.0    2016-09-16
# 2     Lucy    Chow Chow  Brown         46       24.0    2014-08-25
# 3   Cooper    Schnauzer   Gray         49        0.0    2011-12-11
# 4      Max     Labrador  Black         59       29.0    2017-01-20
# 5   Stella    Chihuahua    Tan         18        2.0    2015-04-20
# 6   Bernie  St. Bernard  White         77       74.0    2018-02-27


# =====================================================================
# 8. Creating DataFrames: list of dictionaries vs. dictionary of lists
# =====================================================================

# A plain Python dictionary maps keys to values, looked up by key.
my_dict = {
    "title": "Charlotte's Web",
    "author": "E.B. White",
    "published": 1952,
}
print(my_dict["title"])  # "Charlotte's Web"

# A DataFrame can be built two ways:
#  - from a list of dictionaries: constructed row by row
#  - from a dictionary of lists: constructed column by column

# List of dictionaries: each dict is one row, keys become column names.
list_of_dicts = [
    {"name": "Ginger", "breed": "Dachshund", "height_cm": 22,
     "weight_kg": 10, "date_of_birth": "2019-03-14"},

    {"name": "Scout", "breed": "Dalmatian", "height_cm": 59,
     "weight_kg": 25, "date_of_birth": "2019-05-09"},
]
new_dogs = pd.DataFrame(list_of_dicts)
print(new_dogs)
#      name      breed  height_cm  weight_kg date_of_birth
# 0  Ginger  Dachshund         22         10    2019-03-14
# 1   Scout  Dalmatian         59         25    2019-05-09

# Dictionary of lists: each key is a column name, each value a list of
# that column's values (same order across all the lists).
dict_of_lists = {
    "name": ["Ginger", "Scout"],
    "breed": ["Dachshund", "Dalmatian"],
    "height_cm": [22, 59],
    "weight_kg": [10, 25],
    "date_of_birth": ["2019-03-14", "2019-05-09"],
}
new_dogs = pd.DataFrame(dict_of_lists)
print(new_dogs)
#      name      breed  height_cm  weight_kg date_of_birth
# 0  Ginger  Dachshund         22         10    2019-03-14
# 1   Scout  Dalmatian         59         25    2019-05-09


# =====================================================================
# 9. Reading and writing CSVs
# =====================================================================

# CSV = comma-separated values, designed for exactly this kind of
# rectangular data; most database/spreadsheet software can read and
# write it. new_dogs.csv would look like:
#   name,breed,height_cm,weight_kg,d_o_b
#   Ginger,Dachshund,22,10,2019-03-14
#   Scout,Dalmatian,59,25,2019-05-09

# pd.read_csv() turns a CSV file straight into a DataFrame.
new_dogs = pd.read_csv("new_dogs.csv")
print(new_dogs)
#      name      breed  height_cm  weight_kg date_of_birth
# 0  Ginger  Dachshund         22         10    2019-03-14
# 1   Scout  Dalmatian         59         25    2019-05-09

# A DataFrame loaded from CSV can be manipulated exactly like any other.
new_dogs["bmi"] = new_dogs["weight_kg"] / (new_dogs["height_cm"] / 100) ** 2
print(new_dogs)
#      name      breed  height_cm  weight_kg date_of_birth         bmi
# 0  Ginger  Dachshund         22         10    2019-03-14  206.611570
# 1   Scout  Dalmatian         59         25    2019-05-09   71.818443

# .to_csv() writes a DataFrame back out to a CSV file.
new_dogs.to_csv("new_dogs_with_bmi.csv")
# new_dogs_with_bmi.csv:
#   name,breed,height_cm,weight_kg,d_o_b,bmi
#   Ginger,Dachshund,22,10,2019-03-14,206.611570
#   Scout,Dalmatian,59,25,2019-05-09,71.818443


# =====================================================================
# 10. Wrap-up
# =====================================================================

# Recap:
#   Chapter 1: Subsetting and sorting, adding new columns
#   Chapter 2: Aggregating and grouping, summary statistics
#   Chapter 3: Indexing, slicing
#   Chapter 4: Visualizations, reading and writing CSVs

# Where to go next:
#   Joining Data with pandas
#   Streamlined Data Ingestion with pandas
#   Analyzing Police Activity with pandas
#   Analyzing Marketing Campaigns with pandas
