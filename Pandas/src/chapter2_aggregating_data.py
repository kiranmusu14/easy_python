"""
Aggregating Data
-----------------
Once a DataFrame is built and subset, the next step is to summarize it:
single-number summary statistics, custom summaries via .agg(), running
totals with cumulative statistics, counting (and avoiding double-counting)
categorical data, and computing summaries per group with .groupby() and
.pivot_table().

Table of Contents
1. Summarizing numerical data
2. Summarizing dates
3. The .agg() method for custom and multiple summaries
4. Cumulative statistics
5. Counting: avoiding double-counting with .drop_duplicates()
6. Counting values: .value_counts() and proportions
7. Grouped summary statistics with .groupby()
8. Grouping by multiple variables and multiple columns
9. Pivot tables: .pivot_table() basics
10. Pivot tables: multiple statistics, two variables, fill_value and margins
"""

import pandas as pd

# The same dogs DataFrame introduced in chapter 1.
dogs = pd.DataFrame({
    "name": ["Bella", "Charlie", "Lucy", "Cooper", "Max", "Stella", "Bernie"],
    "breed": ["Labrador", "Poodle", "Chow Chow", "Schnauzer", "Labrador",
              "Chihuahua", "St. Bernard"],
    "color": ["Brown", "Black", "Brown", "Gray", "Black", "Tan", "White"],
    "height_cm": [56, 43, 46, 49, 59, 18, 77],
    "weight_kg": [24, 24, 24, 17, 29, 2, 74],
    "date_of_birth": ["2013-07-01", "2016-09-16", "2014-08-25", "2011-12-11",
                       "2017-01-20", "2015-04-20", "2018-02-27"],
})

# =====================================================================
# 1. Summarizing numerical data
# =====================================================================

# Summary methods take a column (a Series) and return a single number.
print(dogs["height_cm"].mean())  # 49.714285714285715

# Other summary methods work the same way:
#   .median(), .mode()
#   .min(), .max()
#   .var(), .std()
#   .sum()
#   .quantile()


# =====================================================================
# 2. Summarizing dates
# =====================================================================

# .min() / .max() also work on dates, giving the oldest/youngest record.
print(dogs["date_of_birth"].min())  # '2011-12-11' (oldest dog)
print(dogs["date_of_birth"].max())  # '2018-02-27' (youngest dog)


# =====================================================================
# 3. The .agg() method for custom and multiple summaries
# =====================================================================

# .agg() applies a custom summary function (taking a column, returning
# one value) to a column — here, the 30th percentile.
def pct30(column):
    return column.quantile(0.3)


print(dogs["weight_kg"].agg(pct30))  # 22.6

# .agg() also works across multiple columns at once.
print(dogs[["weight_kg", "height_cm"]].agg(pct30))
# weight_kg    22.6
# height_cm    45.4
# dtype: float64

# Passing a list of functions to .agg() returns multiple summaries.
def pct40(column):
    return column.quantile(0.4)


print(dogs["weight_kg"].agg([pct30, pct40]))
# pct30    22.6
# pct40    24.0
# Name: weight_kg, dtype: float64


# =====================================================================
# 4. Cumulative statistics
# =====================================================================

print(dogs["weight_kg"])
# 0    24
# 1    24
# 2    24
# 3    17
# 4    29
# 5     2
# 6    74
# Name: weight_kg, dtype: int64

# .cumsum() returns a running total, one entry per row.
print(dogs["weight_kg"].cumsum())
# 0     24
# 1     48
# 2     72
# 3     89
# 4    118
# 5    120
# 6    194
# Name: weight_kg, dtype: int64

# Related cumulative statistics:
#   .cummax()
#   .cummin()
#   .cumprod()

# The Walmart weekly-sales dataset used in this chapter's exercises is
# much larger than can be reproduced from the slides; it's loaded from
# its own CSV rather than typed out here.
sales = pd.read_csv("sales.csv", parse_dates=["date"])
print(sales.head())
#   store type  dept       date  weekly_sales  is_holiday  temp_c  fuel_price  unemp
# 0     1    A     1 2010-02-05      24924.50       False    5.73       0.679  8.106
# 1     1    A     2 2010-02-05      50605.27       False    5.73       0.679  8.106
# 2     1    A     3 2010-02-05      13740.12       False    5.73       0.679  8.106
# 3     1    A     4 2010-02-05      39954.04       False    5.73       0.679  8.106
# 4     1    A     5 2010-02-05      32229.38       False    5.73       0.679  8.106


# =====================================================================
# 5. Counting: avoiding double-counting with .drop_duplicates()
# =====================================================================

# vet_visits has multiple rows per dog (repeat visits), so counting rows
# would over-count unique dogs. It's a much larger dataset than what's
# shown on the slides, so it's loaded from its own CSV here.
vet_visits = pd.read_csv("vet_visits.csv", parse_dates=["date"])
print(vet_visits)
#           date     name        breed  weight_kg
# 0   2018-09-02    Bella     Labrador      24.87
# 1   2019-06-07      Max     Labrador      28.35
# 2   2018-01-17   Stella    Chihuahua       1.51
# 3   2019-10-19     Lucy    Chow Chow      24.07
# ..         ...      ...          ...        ...
# 71  2018-01-20   Stella    Chihuahua       2.83
# 72  2019-06-07      Max    Chow Chow      24.01
# 73  2018-08-20     Lucy    Chow Chow      24.40
# 74  2019-04-22      Max     Labrador      28.54

# subset="name" keeps only the first visit row for each dog name.
print(vet_visits.drop_duplicates(subset="name"))
#           date     name        breed  weight_kg
# 0   2018-09-02    Bella     Labrador      24.87
# 1   2019-06-07      Max    Chow Chow      24.01
# 2   2019-03-19  Charlie       Poodle      24.95
# 3   2018-01-17   Stella    Chihuahua       1.51
# 4   2019-10-19     Lucy    Chow Chow      24.07
# 7   2019-03-30   Cooper    Schnauzer      16.91
# 10  2019-01-04   Bernie  St. Bernard      74.98


# =====================================================================
# 6. Counting values: .value_counts() and proportions
# =====================================================================

# Dropping duplicate (name, breed) pairs instead of just name gives one
# row per unique dog, even if the same name/breed combination revisits.
unique_dogs = vet_visits.drop_duplicates(subset=["name", "breed"])
print(unique_dogs)
#           date     name        breed  weight_kg
# 0   2018-09-02    Bella     Labrador      24.87
# 1   2019-03-13      Max    Chow Chow      24.13
# 2   2019-03-19  Charlie       Poodle      24.95
# 3   2018-01-17   Stella    Chihuahua       1.51
# 4   2019-10-19     Lucy    Chow Chow      24.07
# 6   2019-06-07      Max     Labrador      28.35
# 7   2019-03-30   Cooper    Schnauzer      16.91
# 10  2019-01-04   Bernie  St. Bernard      74.98

# .value_counts() counts how many times each value occurs in a column.
print(unique_dogs["breed"].value_counts())
# Labrador       2
# Schnauzer      1
# St. Bernard    1
# Chow Chow      2
# Poodle         1
# Chihuahua      1
# Name: breed, dtype: int64

# sort=True orders the counts from most to least common.
print(unique_dogs["breed"].value_counts(sort=True))
# Labrador       2
# Chow Chow      2
# Schnauzer      1
# St. Bernard    1
# Poodle         1
# Chihuahua      1
# Name: breed, dtype: int64

# normalize=True turns counts into proportions of the total instead.
print(unique_dogs["breed"].value_counts(normalize=True))
# Labrador       0.250
# Chow Chow      0.250
# Schnauzer      0.125
# St. Bernard    0.125
# Poodle         0.125
# Chihuahua      0.125
# Name: breed, dtype: float64


# =====================================================================
# 7. Grouped summary statistics with .groupby()
# =====================================================================

# Repeating the same summary once per group by hand doesn't scale.
print(dogs[dogs["color"] == "Black"]["weight_kg"].mean())  # 26.0
print(dogs[dogs["color"] == "Brown"]["weight_kg"].mean())  # 24.0
print(dogs[dogs["color"] == "White"]["weight_kg"].mean())  # 74.0
print(dogs[dogs["color"] == "Gray"]["weight_kg"].mean())   # 17.0
print(dogs[dogs["color"] == "Tan"]["weight_kg"].mean())    # 2.0

# .groupby() does the same thing in one line, one group per color.
print(dogs.groupby("color")["weight_kg"].mean())
# color
# Black    26.5
# Brown    24.0
# Gray     17.0
# Tan       2.0
# White    74.0
# Name: weight_kg, dtype: float64

# Passing a list of functions to .agg() applies each to every group.
print(dogs.groupby("color")["weight_kg"].agg([min, max, sum]))
#        min  max  sum
# color
# Black   24   29   53
# Brown   24   24   48
# Gray    17   17   17
# Tan      2    2    2
# White   74   74   74


# =====================================================================
# 8. Grouping by multiple variables and multiple columns
# =====================================================================

# Passing a list of column names groups by every combination of them.
print(dogs.groupby(["color", "breed"])["weight_kg"].mean())
# color  breed
# Black  Chow Chow      25
#        Labrador       29
#        Poodle         24
# Brown  Chow Chow      24
#        Labrador       24
# Gray   Schnauzer      17
# Tan    Chihuahua       2
# White  St. Bernard    74
# Name: weight_kg, dtype: int64

# Grouping by multiple columns and summarizing multiple columns at once.
print(dogs.groupby(["color", "breed"])[["weight_kg", "height_cm"]].mean())
#                    weight_kg  height_cm
# color breed
# Black Labrador            29         59
#       Poodle              24         43
# Brown Chow Chow           24         46
#       Labrador            24         56
# Gray  Schnauzer           17         49
# Tan   Chihuahua            2         18
# White St. Bernard         74         77


# =====================================================================
# 9. Pivot tables: .pivot_table() basics
# =====================================================================

# .pivot_table() is another way to write a groupby-and-summarize; the
# default aggregation function is the mean.
print(dogs.groupby("color")["weight_kg"].mean())
# color
# Black    26
# Brown    24
# Gray     17
# Tan       2
# White    74
# Name: weight_kg, dtype: int64

print(dogs.pivot_table(values="weight_kg", index="color"))
#        weight_kg
# color
# Black       26.5
# Brown       24.0
# Gray        17.0
# Tan          2.0
# White       74.0

# aggfunc picks a different summary statistic.
print(dogs.pivot_table(values="weight_kg", index="color", aggfunc="median"))
#        weight_kg
# color
# Black       26.5
# Brown       24.0
# Gray        17.0
# Tan          2.0
# White       74.0

# aggfunc can also take a list, to compute several statistics at once.
print(dogs.pivot_table(values="weight_kg", index="color", aggfunc=["mean", "median"]))
#            mean    median
#       weight_kg weight_kg
# color
# Black      26.5      26.5
# Brown      24.0      24.0
# Gray       17.0      17.0
# Tan         2.0       2.0
# White      74.0      74.0


# =====================================================================
# 10. Pivot tables: multiple statistics, two variables, fill_value and margins
# =====================================================================

# Grouping by two variables is equivalent to a pivot table with one
# variable as the index and the other spread across columns.
print(dogs.groupby(["color", "breed"])["weight_kg"].mean())

print(dogs.pivot_table(values="weight_kg", index="color", columns="breed"))
# breed  Chihuahua  Chow Chow  Labrador  Poodle  Schnauzer  St. Bernard
# color
# Black        NaN        NaN      29.0    24.0        NaN          NaN
# Brown        NaN       24.0      24.0     NaN        NaN          NaN
# Gray         NaN        NaN       NaN     NaN       17.0          NaN
# Tan          2.0        NaN       NaN     NaN        NaN          NaN
# White        NaN        NaN       NaN     NaN        NaN         74.0

# fill_value replaces missing color/breed combinations with a given value.
print(dogs.pivot_table(values="weight_kg", index="color", columns="breed",
                        fill_value=0))
# breed  Chihuahua  Chow Chow  Labrador  Poodle  Schnauzer  St. Bernard
# color
# Black          0          0        29      24          0            0
# Brown          0         24        24       0          0            0
# Gray           0          0         0       0         17            0
# Tan            2          0         0       0          0            0
# White          0          0         0       0          0           74

# margins=True adds an "All" row and column with the overall summaries.
print(dogs.pivot_table(values="weight_kg", index="color", columns="breed",
                        fill_value=0, margins=True))
# breed  Chihuahua  Chow Chow  Labrador  Poodle  Schnauzer  St. Bernard        All
# color
# Black          0          0        29      24          0            0  26.500000
# Brown          0         24        24       0          0            0  24.000000
# Gray           0          0         0       0         17            0  17.000000
# Tan            2          0         0       0          0            0   2.000000
# White          0          0         0       0          0           74  74.000000
# All            2         24        26      24         17           74  27.714286
