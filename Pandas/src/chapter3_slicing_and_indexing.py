"""
Slicing and Indexing Data
--------------------------
DataFrames don't have to use the default 0, 1, 2, ... row numbering:
any column (or combination of columns) can become an explicit index.
This chapter covers setting/removing indexes, subsetting and sorting by
index (including multi-level indexes), slicing rows and columns with
.loc and .iloc, and combining slicing with pivot tables.

Table of Contents
1. Setting and removing a column as the index
2. Indexes make subsetting simpler; duplicate index values
3. Multi-level (hierarchical) indexes
4. Sorting by index values
5. Why indexes can be problematic
6. Slicing lists (a quick review)
7. Slicing rows by index with .loc
8. Slicing by dates
9. Slicing columns, and rows and columns together; subsetting by position with .iloc
10. .loc + slicing on pivot tables, and the axis argument
"""

import pandas as pd

# The dogs DataFrame revisited, with the index still the default RangeIndex.
dogs = pd.DataFrame({
    "name": ["Bella", "Charlie", "Lucy", "Cooper", "Max", "Stella", "Bernie"],
    "breed": ["Labrador", "Poodle", "Chow Chow", "Schnauzer", "Labrador",
              "Chihuahua", "St. Bernard"],
    "color": ["Brown", "Black", "Brown", "Gray", "Black", "Tan", "White"],
    "height_cm": [56, 43, 46, 49, 59, 18, 77],
    "weight_kg": [25, 23, 22, 17, 29, 2, 74],
})

print(dogs)
#       name        breed  color  height_cm  weight_kg
# 0    Bella     Labrador  Brown         56         25
# 1  Charlie       Poodle  Black         43         23
# 2     Lucy    Chow Chow  Brown         46         22
# 3   Cooper    Schnauzer   Gray         49         17
# 4      Max     Labrador  Black         59         29
# 5   Stella    Chihuahua    Tan         18          2
# 6   Bernie  St. Bernard  White         77         74


# =====================================================================
# 1. Setting and removing a column as the index
# =====================================================================

print(dogs.columns)
# Index(['name', 'breed', 'color', 'height_cm', 'weight_kg'], dtype='object')
print(dogs.index)  # RangeIndex(start=0, stop=7, step=1)

# .set_index() moves a column out of the data and into the index.
dogs_ind = dogs.set_index("name")
print(dogs_ind)
#                breed  color  height_cm  weight_kg
# name
# Bella       Labrador  Brown         56         25
# Charlie       Poodle  Black         43         23
# Lucy       Chow Chow  Brown         46         22
# Cooper     Schnauzer   Gray         49         17
# Max         Labrador  Black         59         29
# Stella     Chihuahua    Tan         18          2
# Bernie   St. Bernard  White         77         74

# .reset_index() undoes that, moving the index back into a column.
print(dogs_ind.reset_index())
#       name        breed  color  height_cm  weight_kg
# 0    Bella     Labrador  Brown         56         25
# 1  Charlie       Poodle  Black         43         23
# 2     Lucy    Chow Chow  Brown         46         22
# 3   Cooper    Schnauzer   Gray         49         17
# 4      Max     Labrador  Black         59         29
# 5   Stella    Chihuahua    Tan         18          2
# 6   Bernie  St. Bernard  White         77         74

# drop=True discards the old index entirely instead of keeping it as a column.
print(dogs_ind.reset_index(drop=True))
#         breed  color  height_cm  weight_kg
# 0    Labrador  Brown         56         25
# 1      Poodle  Black         43         23
# 2   Chow Chow  Brown         46         22
# 3   Schnauzer   Gray         49         17
# 4    Labrador  Black         59         29
# 5   Chihuahua    Tan         18          2
# 6 St. Bernard  White         77         74


# =====================================================================
# 2. Indexes make subsetting simpler; duplicate index values
# =====================================================================

# Subsetting by name, the old way: a boolean condition with .isin().
print(dogs[dogs["name"].isin(["Bella", "Stella"])])
#      name      breed  color  height_cm  weight_kg
# 0   Bella   Labrador  Brown         56         25
# 5  Stella  Chihuahua    Tan         18          2

# The same subset, using .loc[] with a list of index labels instead.
print(dogs_ind.loc[["Bella", "Stella"]])
#             breed  color  height_cm  weight_kg
# name
# Bella    Labrador  Brown         56         25
# Stella  Chihuahua    Tan         18          2

# Index values don't need to be unique — here breed is used as the index,
# and "Labrador" appears twice.
dogs_ind2 = dogs.set_index("breed")
print(dogs_ind2)
#                 name  color  height_cm  weight_kg
# breed
# Labrador       Bella  Brown         56         25
# Poodle       Charlie  Black         43         23
# Chow Chow       Lucy  Brown         46         22
# Schnauzer     Cooper   Gray         49         17
# Labrador         Max  Black         59         29
# Chihuahua     Stella    Tan         18          2
# St. Bernard   Bernie  White         77         74

# .loc[] on a duplicated index label returns every matching row.
print(dogs_ind2.loc["Labrador"])
#            name  color  height_cm  weight_kg
# breed
# Labrador  Bella  Brown         56         25
# Labrador    Max  Black         59         29


# =====================================================================
# 3. Multi-level (hierarchical) indexes
# =====================================================================

# set_index() accepts a list of columns to build a multi-level index.
dogs_ind3 = dogs.set_index(["breed", "color"])
print(dogs_ind3)
#                       name  height_cm  weight_kg
# breed       color
# Labrador    Brown    Bella         56         25
# Poodle      Black  Charlie         43         23
# Chow Chow   Brown     Lucy         46         22
# Schnauzer   Gray    Cooper         49         17
# Labrador    Black      Max         59         29
# Chihuahua   Tan     Stella         18          2
# St. Bernard White   Bernie         77         74

# Subset the outer index level with a plain list of labels.
print(dogs_ind3.loc[["Labrador", "Chihuahua"]])
#                    name  height_cm  weight_kg
# breed     color
# Labrador  Brown   Bella         56         25
#           Black     Max         59         29
# Chihuahua Tan    Stella         18          2

# Subset combinations of outer + inner levels with a list of tuples.
print(dogs_ind3.loc[[("Labrador", "Brown"), ("Chihuahua", "Tan")]])
#                    name  height_cm  weight_kg
# breed     color
# Labrador  Brown   Bella         56         25
# Chihuahua Tan    Stella         18          2


# =====================================================================
# 4. Sorting by index values
# =====================================================================

# .sort_index() sorts by every index level, outer to inner, by default.
print(dogs_ind3.sort_index())
#                       name  height_cm  weight_kg
# breed       color
# Chihuahua   Tan     Stella         18          2
# Chow Chow   Brown     Lucy         46         22
# Labrador    Black      Max         59         29
#             Brown    Bella         56         25
# Poodle      Black  Charlie         43         23
# Schnauzer   Gray    Cooper         49         17
# St. Bernard White   Bernie         77         74

# level and ascending give control over which levels sort which way.
print(dogs_ind3.sort_index(level=["color", "breed"], ascending=[True, False]))
#                       name  height_cm  weight_kg
# breed       color
# Poodle      Black  Charlie         43         23
# Labrador    Black      Max         59         29
#             Brown    Bella         56         25
# Chow Chow   Brown     Lucy         46         22
# Schnauzer   Gray    Cooper         49         17
# Chihuahua   Tan     Stella         18          2
# St. Bernard White   Bernie         77         74


# =====================================================================
# 5. Why indexes can be problematic
# =====================================================================

# Indexes are a useful shortcut for subsetting, but they come at a cost:
#  - Index values are just data, stored differently from the rest.
#  - Indexes violate "tidy data" principles (each variable a column).
#  - You need to learn two syntaxes: one for columns, one for the index.

# Example of a "tidy" temperature dataset that keeps date/city/country as
# ordinary columns rather than an index (avg_temp_c in degrees Celsius):
#         date      city           country       avg_temp_c
# 0 2000-01-01   Abidjan   Cote D'Ivoire            27.293
# 1 2000-02-01   Abidjan   Cote D'Ivoire            27.685
# 2 2000-03-01   Abidjan   Cote D'Ivoire            29.061
# 3 2000-04-01   Abidjan   Cote D'Ivoire            28.162
# 4 2000-05-01   Abidjan   Cote D'Ivoire            27.547


# =====================================================================
# 6. Slicing lists (a quick review)
# =====================================================================

# Ordinary list slicing works on position, [start:end], end exclusive.
breeds = ["Labrador", "Poodle", "Chow Chow", "Schnauzer", "Labrador",
          "Chihuahua", "St. Bernard"]
print(breeds)
# ['Labrador', 'Poodle', 'Chow Chow', 'Schnauzer', 'Labrador', 'Chihuahua', 'St. Bernard']

print(breeds[2:5])  # ['Chow Chow', 'Schnauzer', 'Labrador']
print(breeds[:3])   # ['Labrador', 'Poodle', 'Chow Chow']
print(breeds[:])    # the whole list, unchanged


# =====================================================================
# 7. Slicing rows by index with .loc
# =====================================================================

# The index must be sorted first, or slicing with .loc gives wrong/empty
# results.
dogs_srt = dogs.set_index(["breed", "color"]).sort_index()
print(dogs_srt)
#                       name  height_cm  weight_kg
# breed       color
# Chihuahua   Tan     Stella         18          2
# Chow Chow   Brown     Lucy         46         22
# Labrador    Black      Max         59         29
#             Brown    Bella         56         25
# Poodle      Black  Charlie         43         23
# Schnauzer   Gray    Cooper         49         17
# St. Bernard White   Bernie         77         74

# Slicing the outer index level works like slicing a sorted list; the
# final value ("Poodle") IS included, unlike list slicing.
print(dogs_srt.loc["Chow Chow":"Poodle"])
#                     name  height_cm  weight_kg
# breed     color
# Chow Chow Brown     Lucy         46         22
# Labrador  Black      Max         59         29
#           Brown    Bella         56         25
# Poodle    Black  Charlie         43         23

# Slicing the INNER level directly (ignoring the outer level) silently
# gives an empty result — it doesn't do what you'd expect.
print(dogs_srt.loc["Tan":"Grey"])
# Empty DataFrame
# Columns: [name, height_cm, weight_kg]
# Index: []

# The correct way to slice inner levels: pass a tuple of
# (outer, inner) labels for both the start and the end.
print(dogs_srt.loc[("Labrador", "Brown"):("Schnauzer", "Gray")])
#                     name  height_cm  weight_kg
# breed     color
# Labrador  Brown    Bella         56         25
# Poodle    Black  Charlie         43         23
# Schnauzer Gray    Cooper         49         17


# =====================================================================
# 8. Slicing by dates
# =====================================================================

# Setting a date column as the index (and sorting it) allows slicing a
# date range with .loc, the same way as slicing any other sorted index.
dogs = dogs.assign(date_of_birth=["2013-07-01", "2016-09-16", "2014-08-25",
                                   "2011-12-11", "2017-01-20", "2015-04-20",
                                   "2018-02-27"])
dogs = dogs.set_index("date_of_birth").sort_index()
print(dogs)
#                   name        breed  color  height_cm  weight_kg
# date_of_birth
# 2011-12-11      Cooper    Schnauzer   Gray         49         17
# 2013-07-01       Bella     Labrador  Brown         56         25
# 2014-08-25        Lucy    Chow Chow  Brown         46         22
# 2015-04-20      Stella    Chihuahua    Tan         18          2
# 2016-09-16     Charlie       Poodle  Black         43         23
# 2017-01-20         Max     Labrador  Black         59         29
# 2018-02-27      Bernie  St. Bernard  White         77         74

# Get dogs with date_of_birth between 2014-08-25 and 2016-09-16 (inclusive).
print(dogs.loc["2014-08-25":"2016-09-16"])
#                   name      breed  color  height_cm  weight_kg
# date_of_birth
# 2014-08-25        Lucy  Chow Chow  Brown         46         22
# 2015-04-20      Stella  Chihuahua    Tan         18          2
# 2016-09-16     Charlie     Poodle  Black         43         23

# A partial date ("2014", "2016") slices by year, matching every date
# that falls inside it: everything from 2014-01-01 to 2016-12-31.
print(dogs.loc["2014":"2016"])
#                  name      breed  color  height_cm  weight_kg
# date_of_birth
# 2014-08-25       Lucy  Chow Chow  Brown         46         22
# 2015-04-20     Stella  Chihuahua    Tan         18          2
# 2016-09-16    Charlie     Poodle  Black         43         23


# =====================================================================
# 9. Slicing columns, and rows and columns together; subsetting by position with .iloc
# =====================================================================

# .loc[rows, columns] — a column slice works the same way as a row slice.
print(dogs_srt.loc[:, "name":"height_cm"])
#                       name  height_cm
# breed       color
# Chihuahua   Tan     Stella         18
# Chow Chow   Brown     Lucy         46
# Labrador    Black      Max         59
#             Brown    Bella         56
# Poodle      Black  Charlie         43
# Schnauzer   Gray    Cooper         49
# St. Bernard White   Bernie         77

# Rows and columns can be sliced at the same time, in a single .loc call.
print(dogs_srt.loc[("Labrador", "Brown"):("Schnauzer", "Gray"),
                    "name":"height_cm"])
#                     name  height_cm
# breed     color
# Labrador  Brown    Bella         56
# Poodle    Black  Charlie         43
# Schnauzer Gray    Cooper         49

# .iloc[] slices by row/column position instead of by label.
print(dogs.iloc[2:5, 1:4])
#        breed  color  height_cm
# 2  Chow Chow  Brown         46
# 3  Schnauzer   Gray         49
# 4   Labrador  Black         59


# =====================================================================
# 10. .loc + slicing on pivot tables, and the axis argument
# =====================================================================

# A larger dog dataset (dog_pack) used for this section's pivot table —
# too large to type out in full, so it's loaded from its own CSV.
dog_pack = pd.read_csv("dog_pack.csv")
print(dog_pack)
#           breed  color  height_cm  weight_kg
# 0         Boxer  Brown      62.64       30.4
# 1        Poodle  Black      46.41       20.4
# 2        Beagle  Brown      36.39       12.4
# 3     Chihuahua    Tan      19.70        1.6
# 4      Labrador    Tan      54.44       36.1
# ..          ...    ...        ...        ...
# 87        Boxer   Gray      58.13       29.9
# 88  St. Bernard  White      70.13       69.4
# 89       Poodle   Gray      51.30       20.4
# 90       Beagle  White      38.81        8.8
# 91       Beagle  Black      33.40       13.5

# A pivot table with breed as rows and color as columns, mean height.
dogs_height_by_breed_vs_color = dog_pack.pivot_table(
    "height_cm", index="breed", columns="color")
print(dogs_height_by_breed_vs_color)
# color            Black    Brown       Gray        Tan      White
# breed
# Beagle       34.500000  36.4500  36.313333  35.740000  38.810000
# Boxer        57.203333  62.6400  58.280000  62.310000  56.360000
# Chihuahua    18.555000      NaN  21.660000  20.096667  17.933333
# Chow Chow    51.262500  50.4800        NaN  53.497500  54.413333
# Dachshund    21.186667  19.7250        NaN  19.375000  20.660000
# Labrador     57.125000      NaN        NaN  55.190000  55.310000
# Poodle       48.036000  57.1300  56.645000        NaN  44.740000
# St. Bernard  63.920000  65.8825  67.640000  68.334000  67.495000

# .loc[] + slicing works on a pivot table's (row) index, same as any
# other DataFrame with a sorted index.
print(dogs_height_by_breed_vs_color.loc["Chow Chow":"Poodle"])
# color          Black   Brown    Gray      Tan      White
# breed
# Chow Chow  51.262500  50.480     NaN  53.4975  54.413333
# Dachshund  21.186667  19.725     NaN  19.3750  20.660000
# Labrador   57.125000     NaN     NaN  55.1900  55.310000
# Poodle     48.036000  57.130  56.645      NaN  44.740000

# axis="index" (the default) summarizes down each column.
print(dogs_height_by_breed_vs_color.mean(axis="index"))
# color
# Black    43.973563
# Brown    48.717917
# Gray     48.107667
# Tan      44.934738
# White    44.465208
# dtype: float64

# axis="columns" summarizes across each row instead.
print(dogs_height_by_breed_vs_color.mean(axis="columns"))
# breed
# Beagle         36.362667
# Boxer          59.358667
# Chihuahua      19.561250
# Chow Chow      52.413333
# Dachshund      20.236667
# Labrador       55.875000
# Poodle         51.637750
# St. Bernard    66.654300
# dtype: float64
