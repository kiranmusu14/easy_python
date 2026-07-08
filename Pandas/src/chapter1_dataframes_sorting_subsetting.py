"""
Introducing DataFrames
-----------------------
pandas is the go-to Python package for working with rectangular ("tidy")
data: rows are observations, columns are variables. This chapter covers
what a DataFrame is and how to explore one, how to sort and subset rows
and columns, and how to add new columns computed from existing ones.

Table of Contents
1. What's the point of pandas?
2. Rectangular data: building the dogs DataFrame
3. Exploring a DataFrame: .head(), .info(), .shape, .describe()
4. Components of a DataFrame: .values, .columns, .index
5. Sorting rows with .sort_values()
6. Subsetting columns
7. Subsetting rows with logical conditions
8. Subsetting rows with multiple conditions and .isin()
9. Adding new columns
10. Multiple manipulations chained together
"""

import pandas as pd

# =====================================================================
# 1. What's the point of pandas?
# =====================================================================

# pandas is built on top of NumPy (fast numerical arrays) and Matplotlib
# (plotting) — it adds labeled, tabular data structures on top of them.
# It's one of the most popular Python packages for data manipulation and
# feeds into both the Data Manipulation and Data Visualization skill tracks.

# Course outline:
#   Chapter 1: DataFrames                      - sorting/subsetting, new columns
#   Chapter 2: Aggregating Data                 - summary stats, counting, groupby
#   Chapter 3: Slicing and Indexing Data         - slicing, indexes
#   Chapter 4: Creating and Visualizing Data     - plotting, missing data, I/O

# pandas philosophy, quoting the Zen of Python:
# "There should be one -- and preferably only one -- obvious way to do it."


# =====================================================================
# 2. Rectangular data: building the dogs DataFrame
# =====================================================================

# Rectangular data: one row per observation (a dog), one column per
# variable (name, breed, color, height, weight, date of birth). A pandas
# DataFrame is built here from a dictionary of lists — one key per column.
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

print(dogs)
#       name        breed  color  height_cm  weight_kg date_of_birth
# 0    Bella     Labrador  Brown         56         24    2013-07-01
# 1  Charlie       Poodle  Black         43         24    2016-09-16
# 2     Lucy    Chow Chow  Brown         46         24    2014-08-25
# 3   Cooper    Schnauzer   Gray         49         17    2011-12-11
# 4      Max     Labrador  Black         59         29    2017-01-20
# 5   Stella    Chihuahua    Tan         18          2    2015-04-20
# 6   Bernie  St. Bernard  White         77         74    2018-02-27


# =====================================================================
# 3. Exploring a DataFrame: .head(), .info(), .shape, .describe()
# =====================================================================

# .head() returns just the first five rows.
print(dogs.head())
#       name        breed  color  height_cm  weight_kg date_of_birth
# 0    Bella     Labrador  Brown         56         24    2013-07-01
# 1  Charlie       Poodle  Black         43         24    2016-09-16
# 2     Lucy    Chow Chow  Brown         46         24    2014-08-25
# 3   Cooper    Schnauzer   Gray         49         17    2011-12-11
# 4      Max     Labrador  Black         59         29    2017-01-20

# .info() reports column names, dtypes, and non-null counts.
print(dogs.info())
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 7 entries, 0 to 6
# Data columns (total 6 columns):
#  #   Column         Non-Null Count  Dtype
#  --  ------         --------------  -----
#  0   name           7 non-null      object
#  1   breed          7 non-null      object
#  2   color          7 non-null      object
#  3   height_cm      7 non-null      int64
#  4   weight_kg      7 non-null      int64
#  5   date_of_birth  7 non-null      object
# dtypes: int64(2), object(4)
# memory usage: 464.0+ bytes

# .shape reports (num_rows, num_columns) — note: an attribute, not a call.
print(dogs.shape)  # (7, 6)

# .describe() computes summary statistics for each numeric column.
print(dogs.describe())
#        height_cm  weight_kg
# count   7.000000   7.000000
# mean   49.714286  27.428571
# std    17.960274  22.292429
# min    18.000000   2.000000
# 25%    44.500000  19.500000
# 50%    49.000000  23.000000
# 75%    57.500000  27.000000
# max    77.000000  74.000000
# NOTE: the weight_kg stats above are copied verbatim from the source
# slide; they don't recompute exactly from the weight_kg values used
# elsewhere in this chapter (24, 24, 24, 17, 29, 2, 74) — an inconsistency
# in the original slide deck rather than something introduced here.


# =====================================================================
# 4. Components of a DataFrame: .values, .columns, .index
# =====================================================================

# .values holds the data as a 2D NumPy array, no row/column labels.
print(dogs.values)
# array([['Bella', 'Labrador', 'Brown', 56, 24, '2013-07-01'],
#        ['Charlie', 'Poodle', 'Black', 43, 24, '2016-09-16'],
#        ['Lucy', 'Chow Chow', 'Brown', 46, 24, '2014-08-25'],
#        ['Cooper', 'Schnauzer', 'Gray', 49, 17, '2011-12-11'],
#        ['Max', 'Labrador', 'Black', 59, 29, '2017-01-20'],
#        ['Stella', 'Chihuahua', 'Tan', 18, 2, '2015-04-20'],
#        ['Bernie', 'St. Bernard', 'White', 77, 74, '2018-02-27']],
#       dtype=object)

# .columns holds the column names; .index holds the row labels.
print(dogs.columns)
# Index(['name', 'breed', 'color', 'height_cm', 'weight_kg', 'date_of_birth'],
#       dtype='object')

print(dogs.index)  # RangeIndex(start=0, stop=7, step=1)


# =====================================================================
# 5. Sorting rows with .sort_values()
# =====================================================================

# Sort by a single column, ascending by default.
print(dogs.sort_values("weight_kg"))
#       name        breed  color  height_cm  weight_kg date_of_birth
# 5   Stella    Chihuahua    Tan         18          2    2015-04-20
# 3   Cooper    Schnauzer   Gray         49         17    2011-12-11
# 0    Bella     Labrador  Brown         56         24    2013-07-01
# 1  Charlie       Poodle  Black         43         24    2016-09-16
# 2     Lucy    Chow Chow  Brown         46         24    2014-08-25
# 4      Max     Labrador  Black         59         29    2017-01-20
# 6   Bernie  St. Bernard  White         77         74    2018-02-27

# ascending=False reverses the order.
print(dogs.sort_values("weight_kg", ascending=False))
#       name        breed  color  height_cm  weight_kg date_of_birth
# 6   Bernie  St. Bernard  White         77         74    2018-02-27
# 4      Max     Labrador  Black         59         29    2017-01-20
# 0    Bella     Labrador  Brown         56         24    2013-07-01
# 1  Charlie       Poodle  Black         43         24    2016-09-16
# 2     Lucy    Chow Chow  Brown         46         24    2014-08-25
# 3   Cooper    Schnauzer   Gray         49         17    2011-12-11
# 5   Stella    Chihuahua    Tan         18          2    2015-04-20

# Passing a list sorts by the first column, breaking ties with the next.
print(dogs.sort_values(["weight_kg", "height_cm"]))
#       name        breed  color  height_cm  weight_kg date_of_birth
# 5   Stella    Chihuahua    Tan         18          2    2015-04-20
# 3   Cooper    Schnauzer   Gray         49         17    2011-12-11
# 1  Charlie       Poodle  Black         43         24    2016-09-16
# 2     Lucy    Chow Chow  Brown         46         24    2014-08-25
# 0    Bella     Labrador  Brown         56         24    2013-07-01
# 4      Max     Labrador  Black         59         29    2017-01-20
# 6   Bernie  St. Bernard  White         77         74    2018-02-27

# A separate ascending list controls the sort direction per column.
print(dogs.sort_values(["weight_kg", "height_cm"], ascending=[True, False]))
#       name        breed  color  height_cm  weight_kg date_of_birth
# 5   Stella    Chihuahua    Tan         18          2    2015-04-20
# 3   Cooper    Schnauzer   Gray         49         17    2011-12-11
# 0    Bella     Labrador  Brown         56         24    2013-07-01
# 2     Lucy    Chow Chow  Brown         46         24    2014-08-25
# 1  Charlie       Poodle  Black         43         24    2016-09-16
# 4      Max     Labrador  Black         59         29    2017-01-20
# 6   Bernie  St. Bernard  White         77         74    2018-02-27


# =====================================================================
# 6. Subsetting columns
# =====================================================================

# A single column name returns a Series.
print(dogs["name"])
# 0      Bella
# 1    Charlie
# 2       Lucy
# 3     Cooper
# 4        Max
# 5     Stella
# 6     Bernie
# Name: name, dtype: object

# A list of column names returns a DataFrame with just those columns.
print(dogs[["breed", "height_cm"]])
#          breed  height_cm
# 0     Labrador         56
# 1       Poodle         43
# 2    Chow Chow         46
# 3    Schnauzer         49
# 4     Labrador         59
# 5    Chihuahua         18
# 6  St. Bernard         77

# The list of column names can be stored in a variable first.
cols_to_subset = ["breed", "height_cm"]
print(dogs[cols_to_subset])


# =====================================================================
# 7. Subsetting rows with logical conditions
# =====================================================================

# A comparison on a column produces a Series of booleans.
print(dogs["height_cm"] > 50)
# 0     True
# 1    False
# 2    False
# 3    False
# 4     True
# 5    False
# 6     True
# Name: height_cm, dtype: bool

# Passing that boolean Series into [] keeps only the True rows.
print(dogs[dogs["height_cm"] > 50])
#      name        breed  color  height_cm  weight_kg date_of_birth
# 0   Bella     Labrador  Brown         56         24    2013-07-01
# 4     Max     Labrador  Black         59         29    2017-01-20
# 6  Bernie  St. Bernard  White         77         74    2018-02-27

# The same pattern works for text ...
print(dogs[dogs["breed"] == "Labrador"])
#      name        breed  color  height_cm  weight_kg date_of_birth
# 0   Bella     Labrador  Brown         56         24    2013-07-01
# 4     Max     Labrador  Black         59         29    2017-01-20

# ... and for dates (compared here as plain strings).
print(dogs[dogs["date_of_birth"] < "2015-01-01"])
#      name      breed  color  height_cm  weight_kg date_of_birth
# 0   Bella   Labrador  Brown         56         24    2013-07-01
# 2    Lucy  Chow Chow  Brown         46         24    2014-08-25
# 3  Cooper  Schnauzer   Gray         49         17    2011-12-11


# =====================================================================
# 8. Subsetting rows with multiple conditions and .isin()
# =====================================================================

# Combine two boolean Series with & (logical AND) for multiple conditions.
is_lab = dogs["breed"] == "Labrador"
is_brown = dogs["color"] == "Brown"
print(dogs[is_lab & is_brown])
#      name        breed  color  height_cm  weight_kg date_of_birth
# 0   Bella     Labrador  Brown         56         24    2013-07-01

# The same condition written inline, without intermediate variables.
print(dogs[(dogs["breed"] == "Labrador") & (dogs["color"] == "Brown")])

# .isin() checks membership in a list of allowed values in one go,
# instead of chaining several == conditions with |.
is_black_or_brown = dogs["color"].isin(["Black", "Brown"])
print(dogs[is_black_or_brown])
#       name      breed  color  height_cm  weight_kg date_of_birth
# 0    Bella   Labrador  Brown         56         24    2013-07-01
# 1  Charlie     Poodle  Black         43         24    2016-09-16
# 2     Lucy  Chow Chow  Brown         46         24    2014-08-25
# 4      Max   Labrador  Black         59         29    2017-01-20


# =====================================================================
# 9. Adding new columns
# =====================================================================

# Assigning to a new column name creates it, computed from existing columns.
dogs["height_m"] = dogs["height_cm"] / 100
print(dogs)
#       name        breed  color  height_cm  weight_kg date_of_birth  height_m
# 0    Bella     Labrador  Brown         56         24    2013-07-01      0.56
# 1  Charlie       Poodle  Black         43         24    2016-09-16      0.43
# 2     Lucy    Chow Chow  Brown         46         24    2014-08-25      0.46
# 3   Cooper    Schnauzer   Gray         49         17    2011-12-11      0.49
# 4      Max     Labrador  Black         59         29    2017-01-20      0.59
# 5   Stella    Chihuahua    Tan         18          2    2015-04-20      0.18
# 6   Bernie  St. Bernard  White         77         74    2018-02-27      0.77

# "Doggy mass index": BMI = weight in kg / (height in m) ** 2.
dogs["bmi"] = dogs["weight_kg"] / dogs["height_m"] ** 2
print(dogs.head())
#       name      breed  color  height_cm  weight_kg date_of_birth  height_m         bmi
# 0    Bella   Labrador  Brown         56         24    2013-07-01      0.56   76.530612
# 1  Charlie     Poodle  Black         43         24    2016-09-16      0.43  129.799892
# 2     Lucy  Chow Chow  Brown         46         24    2014-08-25      0.46  113.421550
# 3   Cooper  Schnauzer   Gray         49         17    2011-12-11      0.49   70.803832
# 4      Max   Labrador  Black         59         29    2017-01-20      0.59   83.309394


# =====================================================================
# 10. Multiple manipulations chained together
# =====================================================================

# Subsetting, sorting, and column-selecting can be chained step by step,
# each building on the DataFrame produced by the previous line.
bmi_lt_100 = dogs[dogs["bmi"] < 100]
bmi_lt_100_height = bmi_lt_100.sort_values("height_cm", ascending=False)
print(bmi_lt_100_height[["name", "height_cm", "bmi"]])
#      name  height_cm        bmi
# 4     Max         59  83.309394
# 0   Bella         56  76.530612
# 3  Cooper         49  70.803832
# 5  Stella         18  61.728395
